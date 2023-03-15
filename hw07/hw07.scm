(define (cddr s) (cdr (cdr s)))

(define (cadr s) 
    (car 
        (cdr s)
    )
)

(define (caddr s) 
    car(
        (cddr s)
    )
)

(define (ascending? asc-lst) 
    (cond
        (
            (null? (cdr asc-lst)) 
            #t
        )
        (
            (> (car asc-lst) (cadr asc-lst))
            #f
        )
        (else (ascending? (cddr asc-lst)))
    )
)

(define (square n) (* n n))

(define (pow base exp) 
    (cond 
        ((= exp 0)
            0
        )
        ((= exp 1)
            base
        )
        ((odd? exp)
            (* 
                base 
                (square
                    (pow 
                        base
                        (/ (- exp 1) 2)
                    )
                )
            )
        )
        (else 
            (square
                (pow 
                    base
                    (/ exp 2)
                )
            )
        )
    )
)
