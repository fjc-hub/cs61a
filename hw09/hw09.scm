(define-macro (when condition exprs)
  (if (eval condition)
    (cons 'begin exprs)
    ''okay)
)

; FAIL VERSION
; (define-macro (switch expr cases)
;     (cons 'begin 
;       (car  (filter (lambda (case) (= (eval expr) (car case)))
;               cases
;             )
;       )
;     )
; )

(define-macro (switch expr cases)
    (cons 'cond
		(map (lambda (case) (cons `(equal? ,expr (quote ,(car case))) (cdr case))) cases))
)