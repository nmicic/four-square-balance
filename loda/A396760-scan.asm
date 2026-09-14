; A396760: Positive integers k at which A122921(k) - ceiling(sqrt(k/4)) reaches a new record value.
; Submitted by Nenad Micic
; 1,11,53,96,224,384,896,1536,2816,3584,6144,11264,14336,24576,45056,57344,98304,180224,229376,393216,720896,917504,1572864,2883584,3670016,6291456,11534336,14680064,25165824,46137344,58720256,100663296,184549376,234881024,402653184,738197504,939524096
; Direct scan from the definition: the LODA counterpart of the PARI program
; in the OEIS entry (program.gp in sequences/gap-record-locations). This is
; the definitional program; A396760.asm, submitted to LODA instead, uses the
; conjectured recurrence because this scan exceeds LODA's step budget.
; It walks k = 1, 2, 3, ... and for each k
; finds A(k) = A122921(k): the least x >= ceiling(sqrt(k/4)) such that
; k - x^2 = y^2 + z^2 + w^2 with x >= y >= z >= w >= 0. The search over
; (y, z) uses the ordering bounds 3*y^2 >= k - x^2 and 2*z^2 >= k - x^2 - y^2.
; The scan stops at the n-th k whose gap A(k) - ceiling(sqrt(k/4)) exceeds
; every earlier gap. The loop ceiling 16^n only bounds the scan and is never
; reached. The scan reproduces the verified b-file (checked to 17 terms) but
; is slow: term 15 needs more than the default 10^8 steps, so evaluate with
; loda eval A396760-scan.asm -t 17 -c -1.

#offset 1

mov $1,$0
mov $2,0
mov $3,-1
mov $4,16
pow $4,$0
lpb $4
  sub $4,1
  add $2,1
  mov $7,$2
  sub $7,1
  nrt $7,2
  div $7,2
  add $7,1
  mov $5,$7
  mov $6,$2
  nrt $6,2
  sub $6,$7
  add $6,1
  lpb $6
    sub $6,1
    mov $8,$5
    pow $8,2
    mov $15,$2
    trn $15,$8
    mov $8,$15
    mov $11,$8
    equ $11,0
    mov $9,$8
    nrt $9,2
    min $9,$5
    mov $15,$8
    add $15,2
    div $15,3
    mov $16,$15
    nrt $16,2
    mov $17,$16
    pow $17,2
    neq $17,$15
    add $16,$17
    mov $10,$9
    sub $10,$16
    add $10,1
    max $10,0
    lpb $10
      sub $10,1
      mov $12,$9
      pow $12,2
      mov $15,$8
      trn $15,$12
      mov $12,$15
      mov $15,$12
      equ $15,0
      add $11,$15
      mov $13,$12
      nrt $13,2
      min $13,$9
      mov $15,$12
      add $15,1
      div $15,2
      mov $16,$15
      nrt $16,2
      mov $17,$16
      pow $17,2
      neq $17,$15
      add $16,$17
      mov $14,$13
      sub $14,$16
      add $14,1
      max $14,0
      lpb $14
        sub $14,1
        mov $15,$13
        pow $15,2
        mov $16,$12
        trn $16,$15
        mov $17,$16
        nrt $17,2
        pow $17,2
        equ $17,$16
        add $11,$17
        sub $13,1
        mov $15,$11
        equ $15,0
        mul $14,$15
      lpe
      sub $9,1
      mov $15,$11
      equ $15,0
      mul $10,$15
    lpe
    mov $15,$11
    equ $15,0
    add $5,$15
    mul $6,$15
  lpe
  mov $8,$5
  sub $8,$7
  mov $9,$8
  mov $10,$3
  add $10,1
  geq $9,$10
  mov $10,$8
  sub $10,$3
  mul $10,$9
  add $3,$10
  sub $1,$9
  mov $9,$1
  neq $9,0
  mul $4,$9
lpe
mov $0,$2
