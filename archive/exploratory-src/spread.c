/* spread.c -- a companion balance objective: minimal spread s(n) = min over four-square reps
 * (x>=y>=z>=w>=0, x^2+y^2+z^2+w^2=n) of (x - w). The "water-leveling" decomposition.
 * Exact via s(n) = min_w [ f(w) - w ], f(w) = min largest part with all parts >= w.
 * Fast: QR-filtered perfect-square test + pruned w/x loops. u64 only (valid for n < 2^62).
 *
 * build: gcc -O3 -march=native -flto -fopenmp spread.c -o spread -lm
 * run:   ./spread <n>                 # print s(n) and the tightest tuple
 *        ./spread --check N           # validate s(n) by full enumeration on 1..N
 *        ./spread --records N [LO G0] # stream spread-records (n s) over [LO,N]
 *        ./spread --bin LO HI PREFIX  # write (x,y,z,w) of the min-spread rep, n=LO..HI
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <omp.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
static uint8_t SQ256[256],SQ63[63],SQ25[25],SQ11[11];
static void sqi(void){for(int i=0;i<256;i++)SQ256[(i*i)&255]=1;for(int i=0;i<63;i++)SQ63[(i*i)%63]=1;
  for(int i=0;i<25;i++)SQ25[(i*i)%25]=1;for(int i=0;i<11;i++)SQ11[(i*i)%11]=1;}
static inline u64 isq64(u64 x){if(!x)return 0;u64 r=(u64)sqrtl((long double)x);
  while(r>1&&r>x/r)r--;while((r+1)<=x/(r+1))r++;return r;}
static inline int issq(u64 x){if(!SQ256[x&255]||!SQ63[x%63]||!SQ25[x%25]||!SQ11[x%11])return 0;
  u64 r=isq64(x);return r*r==x;}

/* minimal spread of n; writes tightest tuple to out[4]. (u64 path: n < ~4.6e18) */
static int sval(u64 n, u64 out[4]){
    u64 root=isq64(n/4);                 /* approx common level */
    int best=0x7fffffff;
    for(long long w=root; w>=0; w--){
        if(4*(u128)w*w>n) continue;      /* need 4 parts >= w */
        if((long long)(isq64((n+3)/4)) - w >= best) break;   /* lb on spread; w only shrinks */
        u64 r1=n-(u64)w*w;               /* x^2+y^2+z^2, parts in [w,x] */
        u64 xlo=isq64(r1/3); while(3*xlo*xlo<r1) xlo++; if((u64)w>xlo) xlo=w;
        for(u64 x=xlo; (long long)(x-w)<best; x++){
            u64 x2=x*x; if(x2>r1) break;
            u64 m2=r1-x2;                 /* y^2+z^2, w<=z<=y<=x */
            if(m2 > 2*x*x) continue;      /* y,z <= x */
            if(m2 < 2*(u64)w*w) break;    /* y,z >= w impossible for larger x too */
            u64 yhi=isq64(m2); if(yhi>x) yhi=x;
            u64 ylo=isq64(m2/2); while(ylo*ylo*2<m2) ylo++;
            for(u64 y=ylo; y<=yhi; y++){  /* y = larger of the pair */
                u64 z2=m2-y*y; if(!issq(z2)) continue;
                u64 z=isq64(z2); if(z<(u64)w||z>y) continue;
                if((int)(x-w)<best){best=x-w; out[0]=x;out[1]=y;out[2]=z;out[3]=w;}
                goto nextw;               /* min x for this w found */
            }
        }
        nextw:;
    }
    return best;
}

/* reference: minimal spread by FULL enumeration (independent of sval; for --check).
 * Signed loops (no unsigned underflow); enumerates every x>=y>=z>=w>=0 with
 * sum of squares = n and takes the TRUE minimum spread x-w. O(n) per n. */
static int sval_brute(u64 n,u64 o[4]){
    int best=0x7fffffff; long long L=(long long)isq64(n);
    for(long long x=L; x>=0; x--){
        if(4*(u128)x*x < n) break;                 /* x is the max: x >= ceil(sqrt(n/4)) */
        u64 x2=(u64)x*x; if(x2>n) continue;
        for(long long y=x; y>=0; y--){
            u64 r=x2+(u64)y*y; if(r>n) continue;
            for(long long z=y; z>=0; z--){
                u64 r2=r+(u64)z*z; if(r2>n) continue;
                u64 w2=n-r2, w=isq64(w2);
                if(w*w==w2 && (long long)w<=z){
                    int sp=(int)(x-(long long)w);
                    if(sp<best){best=sp; o[0]=x;o[1]=y;o[2]=z;o[3]=w;}
                }
            }
        }
    }
    return best;
}

int main(int c,char**v){
    sqi();
    if(c>=3&&!strcmp(v[1],"--check")){
        u64 N=strtoull(v[2],0,10); int bad=0;
        for(u64 n=1;n<=N;n++){u64 a[4],b[4]; int s1=sval(n,a),s2=sval_brute(n,b);
            u64 sa=a[0]*a[0]+a[1]*a[1]+a[2]*a[2]+a[3]*a[3];
            if(s1!=s2||sa!=n){bad++; if(bad<8)printf("BAD n=%llu fast=%d brute=%d tuple(%llu,%llu,%llu,%llu)\n",
                (unsigned long long)n,s1,s2,(unsigned long long)a[0],(unsigned long long)a[1],(unsigned long long)a[2],(unsigned long long)a[3]);}}
        printf("s(n) --check 1..%llu: %s (bad=%d)\n",(unsigned long long)N,bad?"FAIL":"OK",bad); return 0;
    }
    if(c>=3&&!strcmp(v[1],"--records")){
        u64 N=strtoull(v[2],0,10), LO=c>3?strtoull(v[3],0,10):1; int gbest=c>4?atoi(v[4]):-1;
        if(LO<1) LO=1;
        if(N<LO){ fprintf(stderr,"empty range\n"); return 1; }
        printf("# spread records (n s) in [%llu,%llu]\n",(unsigned long long)LO,(unsigned long long)N);
        #define CH 1000000ULL
        int*S=malloc(CH*sizeof(int)); if(!S){ fprintf(stderr,"OOM\n"); return 1; } u64 z=0;
        for(u64 base=LO;base<=N;base+=CH){u64 hi=base+CH-1; if(hi>N)hi=N; u64 cnt=hi-base+1;
            #pragma omp parallel for schedule(dynamic,2048)
            for(u64 i=0;i<cnt;i++){u64 o[4]; S[i]=sval(base+i,o);}
            for(u64 i=0;i<cnt;i++){ if(S[i]==0)z++; if(S[i]>gbest){gbest=S[i];
                printf("%llu %d\n",(unsigned long long)(base+i),S[i]); fflush(stdout);} }
            fprintf(stderr,"  ...%llu rec=%d zeros=%llu\n",(unsigned long long)hi,gbest,(unsigned long long)z);
        }
        free(S); return 0;
    }
    if(c>=5&&!strcmp(v[1],"--bin")){
        u64 LO=strtoull(v[2],0,10),HI=strtoull(v[3],0,10);
        if(HI<LO){ fprintf(stderr,"--bin: need HI>=LO\n"); return 1; }
        char fb[512]; snprintf(fb,sizeof fb,"%s.xyzw.bin",v[4]);
        FILE*f=fopen(fb,"wb"); if(!f){ fprintf(stderr,"cannot open %s\n",fb); return 1; }
        u64 cnt=HI-LO+1; uint32_t*B=malloc(cnt*16);
        if(!B){ fclose(f); fprintf(stderr,"OOM (%llu rows)\n",(unsigned long long)cnt); return 1; }
        #pragma omp parallel for schedule(dynamic,4096)
        for(u64 i=0;i<cnt;i++){u64 o[4]; sval(LO+i,o); uint32_t*r=&B[4*i];
            r[0]=o[0];r[1]=o[1];r[2]=o[2];r[3]=o[3];}
        fwrite(B,16,cnt,f); fclose(f); free(B);
        fprintf(stderr,"wrote %s (%llu)\n",fb,(unsigned long long)cnt); return 0;
    }
    if(c<2){ fprintf(stderr,"usage: spread <n> | --check N | --records N [LO G0] | --bin LO HI PREFIX\n"); return 1; }
    u64 n=strtoull(v[1],0,10),o[4]; int s=sval(n,o);
    printf("n=%llu  s(n)=%d  tightest=(%llu,%llu,%llu,%llu)  sum=%llu\n",(unsigned long long)n,s,
        (unsigned long long)o[0],(unsigned long long)o[1],(unsigned long long)o[2],(unsigned long long)o[3],
        (unsigned long long)(o[0]*o[0]+o[1]*o[1]+o[2]*o[2]+o[3]*o[3]));
    return 0;
}
