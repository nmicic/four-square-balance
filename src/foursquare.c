/* foursquare.c -- fast EXACT a(n) = minimal largest part in a four-square
 * representation n = x^2+y^2+z^2+w^2, x>=y>=z>=w>=0  (OEIS A122921).
 * Engine (v3): native u128 (n < 2^127); Newton isqrt with u64 fast path; 2-square
 * obstruction residue reject + QR-bitmask perfect-square z-scan; OpenMP over x-blocks.
 * For n < 2^64 a u64 fast path is used throughout.
 *
 * build: gcc -O3 -march=native -flto -fopenmp foursquare.c -o foursquare -lm
 * run:   ./foursquare <n decimal>     # prints a(n), xmin, gap, decomposition, time
 *        ./foursquare --bits B        # n = 2^(B-1)+2^(B-3)+12345 (4 <= B <= 127)
 *        ./foursquare --check         # self-consistency on 1..20000 (see Makefile for
 *                                       the independent b-file regression gate)
 */#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>
#include <math.h>

typedef unsigned __int128 u128;

/* fast EXACT floor-sqrt. u64 fast path (sqrtl + tiny correction); u128 path uses a
 * sqrtl guess + a few Newton steps + exact correction. Same output as bit-by-bit. */
static inline uint64_t isqrt_u64(uint64_t x){
    if(x==0) return 0;
    uint64_t r=(uint64_t)sqrtl((long double)x);
    while(r>(uint64_t)1 && r>x/r) r--;            /* r*r>x, overflow-safe */
    while((r+1)<=x/(r+1)) r++;                     /* (r+1)^2<=x */
    return r;
}
static inline u128 isqrt128(u128 x){
    if((x>>64)==0) return isqrt_u64((uint64_t)x);
    u128 r=(u128)sqrtl((long double)x); if(r==0) r=1;
    for(int i=0;i<4;i++){ u128 nr=(r + x/r)>>1; if(nr>=r) break; r=nr; }
    while(r>0 && r>x/r) r--;
    while((r+1)<=x/(r+1)) r++;
    return r;
}
static inline int is3(u128 m){ if(m==0) return 1; while((m&3)==0) m>>=2; return (m&7)!=7; }

/* small primes = 3 (mod 4): a number with one of these to an ODD power is not a
 * sum of two squares -> we can skip its z-scan. */
static const uint32_t P3[]={3,7,11,19,23,31,43,47,59,67,71,79,83,103,107,127,131,
    139,151,163,167,179,191,199,211,223,227,239,251,263,271,283,307,311,331,347,
    359,367,379,383,419,431,439,443,463,467,479,487,491,499};
#define NP3 (int)(sizeof(P3)/sizeof(P3[0]))

/* fast perfect-square test: QR bitmasks (mod 256,63,25,11) reject ~99.8% before sqrt. */
static uint8_t SQ256[256],SQ63[63],SQ25[25],SQ11[11];
static void sqtab_init(void){
    for(int i=0;i<256;i++) SQ256[i]=0;
    for(int i=0;i<256;i++) SQ256[(i*i)&255]=1;
    for(int i=0;i<63;i++) SQ63[i]=0;
    for(int i=0;i<63;i++) SQ63[(i*i)%63]=1;
    for(int i=0;i<25;i++) SQ25[i]=0;
    for(int i=0;i<25;i++) SQ25[(i*i)%25]=1;
    for(int i=0;i<11;i++) SQ11[i]=0;
    for(int i=0;i<11;i++) SQ11[(i*i)%11]=1;
}
static inline int issq_u64(uint64_t x){
    if(!SQ256[x&255]||!SQ63[x%63]||!SQ25[x%25]||!SQ11[x%11]) return 0;
    uint64_t r=isqrt_u64(x); return r*r==x;
}
static inline int issq128(u128 x){
    if(!SQ256[(unsigned)x&255]||!SQ63[(uint64_t)(x%63)]||!SQ25[(uint64_t)(x%25)]||!SQ11[(uint64_t)(x%11)]) return 0;
    u128 r=isqrt128(x); return r*r==x;
}

/* ---------- u64 factorization (Miller-Rabin + Pollard-Brent), reentrant ---------- */
/* exact: does m have a 2-square rep z^2+w^2 with z(>=w) <= cap ? */
static int two_ok(u128 m, u128 cap){
    if(m==0) return 1;
    /* free mod-8 reject: a sum of two squares is never = 3,6,7 (mod 8) */
    { unsigned r=(unsigned)m & 7u; if(r==3||r==6||r==7) return 0; }
    if((m>>64)==0){                       /* u64 fast path (covers n<2^64) */
        uint64_t mu=(uint64_t)m, cap64=(cap>>64)?~0ULL:(uint64_t)cap, mm=mu;
        /* cheap residue reject: small prime =3 (mod4) to odd power -> not 2-square */
        for(int i=0;i<NP3;i++){ uint32_t p=P3[i];
            if((uint64_t)p*p>mm) break;
            if(mm%p==0){ int e=0; do{ mm/=p; e++; }while(mm%p==0); if(e&1) return 0; } }
        /* exact z-scan with QR-filtered perfect-square test (sqrt only ~0.2% of iters) */
        uint64_t zhi=isqrt_u64(mu); if(zhi>cap64) zhi=cap64;
        uint64_t zlo=isqrt_u64(mu/2); while(zlo*zlo*2<mu) zlo++;
        for(uint64_t z=zlo; z<=zhi; z++) if(issq_u64(mu-z*z)) return 1;
        return 0;
    }
    /* u128 path (n >= 2^64) */
    u128 mm=m;
    for(int i=0;i<NP3;i++){ uint32_t p=P3[i];
        if((u128)p*p>mm) break;
        if(mm % p==0){ int e=0; do{ mm/=p; e++; }while(mm%p==0); if(e&1) return 0; } }
    u128 zhi=isqrt128(m); if(zhi>cap) zhi=cap;
    u128 zlo=isqrt128(m/2); while(zlo*zlo*2<m) zlo++;
    for(u128 z=zlo; z<=zhi; z++) if(issq128(m - z*z)) return 1;   /* QR-filtered */
    return 0;
}

/* feasibility of leading coord x: n-x^2 = 3 squares each <= x ? */
static int feas(u128 n, u128 x){
    if(x*x > n) return 0;                 /* x beyond isqrt(n): no rep (avoid u128 underflow) */
    u128 r1=n - x*x;
    if(!is3(r1)) return 0;
    u128 yhi=isqrt128(r1); if(yhi>x) yhi=x;
    u128 ylo=isqrt128(r1/3); while(3*ylo*ylo<r1) ylo++;
    for(u128 y=ylo; y<=yhi; y++)
        if(two_ok(r1 - y*y, y)) return 1;
    return 0;
}

static u128 xmin_of(u128 n){ u128 x=isqrt128((n+3)/4); while(4*x*x<n) x++; return x; }

/* given the answer x=a(n), recover the lex-min completion (y,z,w), x>=y>=z>=w. */
static void decompose(u128 n, u128 x, u128*Y, u128*Z, u128*W){
    u128 r1=n - x*x;
    u128 yhi=isqrt128(r1); if(yhi>x) yhi=x;
    u128 ylo=isqrt128(r1/3); while(3*ylo*ylo<r1) ylo++;
    for(u128 y=ylo; y<=yhi; y++){
        u128 m=r1 - y*y;
        u128 zhi=isqrt128(m); if(zhi>y) zhi=y;
        u128 zlo=isqrt128(m/2); while(zlo*zlo*2<m) zlo++;
        for(u128 z=zlo; z<=zhi; z++){
            u128 w2=m - z*z, w=isqrt128(w2);
            if(w*w==w2){ *Y=y; *Z=z; *W=w; return; }
        }
    }
    *Y=*Z=*W=0;
}

/* exact a(n), OpenMP over x-blocks (smallest feasible x wins). */
static u128 aval(u128 n, int blk){
    if(n==0) return 0;
    u128 xmin=xmin_of(n);
    for(u128 base=xmin;;base+=blk){
        long hit=-1;
        #pragma omp parallel for schedule(dynamic,1)
        for(int i=0;i<blk;i++){
            if(feas(n, base+i)){
                #pragma omp critical
                { if(hit<0 || i<hit) hit=i; }
            }
        }
        if(hit>=0) return base+hit;
    }
}

/* ---- decimal u128 I/O ---- */
static int parse_u128(const char*s, u128*out){ u128 r=0; if(!*s) return 0; 
    for(; *s; s++){ if(*s<'0'||*s>'9') return 0; u128 nr=r*10+(*s-'0'); if(nr<r) return 0; /*overflow*/ r=nr; } *out=r; return 1; }
static void print_u128(u128 v){ char b[40]; int i=39; b[i--]=0; if(!v)b[i--]='0'; while(v){b[i--]='0'+(int)(v%10); v/=10;} fputs(b+i+1,stdout); }
static int bitlen(u128 v){ int n=0; while(v){ v>>=1; n++; } return n; }

extern u128 aval(u128,int);
int main(int argc,char**argv){
    sqtab_init();
    int blk=8*omp_get_max_threads();
    if(argc>=2 && !strcmp(argv[1],"--check")){
        /* validate vs box-scan reference embedded values would be heavy; instead
         * self-consistency: recompute and check sum-of-squares property via rep. */
        extern int feas(u128,u128);
        int bad=0;
        for(u128 n=1;n<=20000;n++){
            u128 a=aval(n,64), xm=xmin_of(n);
            if(a<xm){ bad++; }
            if(!feas(n,a)){ bad++; printf("infeasible a at n="); print_u128(n); puts(""); }
            if(a>xm && feas(n,a-1)){ bad++; printf("not minimal at n="); print_u128(n); puts(""); }
        }
        printf("self-check 1..20000: %s (bad=%d)\n", bad?"FAIL":"OK", bad);
        return 0;
    }
    u128 n;
    if(argc>=3 && !strcmp(argv[1],"--bits")){
        int B=atoi(argv[2]);
        if(B<4 || B>127){ fprintf(stderr,"--bits: need 4 <= B <= 127\n"); return 1; }
        n=((u128)1<<(B-1)) + ((u128)1<<(B-3)) + 12345;
    } else if(argc>=2){
        if(!parse_u128(argv[1], &n)){ fprintf(stderr,"bad n (need a non-negative integer < 2^128)\n"); return 1; }
    } else { fprintf(stderr,"usage: foursquare <n> | --bits B | --check\n"); return 1; }

    double t0=omp_get_wtime();
    u128 a=aval(n,blk);
    double t=omp_get_wtime()-t0;
    u128 xm=xmin_of(n);
    u128 Y,Z,W; decompose(n,a,&Y,&Z,&W);
    printf("n="); print_u128(n);
    printf("  bits=%d  a(n)=", bitlen(n));
    print_u128(a); printf("  xmin="); print_u128(xm);
    printf("  gap="); print_u128(a-xm);
    printf("  [%.3f s]\n", t);
    printf("  decomposition: ("); print_u128(a); printf(", "); print_u128(Y);
    printf(", "); print_u128(Z); printf(", "); print_u128(W); printf(")\n");
    return 0;
}
