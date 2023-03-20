(define (my-filter pred s) 
	(if (null? s)
		s
		(let ((first (car s)) (rest (cdr s)))
			(if (pred first)
				(cons first (my-filter pred rest))
				(my-filter pred rest)
			)
		)
	)
)

(define (interleave lst1 lst2) 
	(cond 
		((null? lst1) lst2)
		((null? lst2) lst1)
		(else 
			(append 
				(list (car lst1))
				(list (car lst2))
				(interleave (cdr lst1) (cdr lst2))
			)
		)
	)
)

; joiner will always be commutative
(define (accumulate joiner start n term)
	(if (= n 1)
		(joiner start (term n))
		(accumulate joiner 
			(joiner start (term n))
			(- n 1)
			term
		)
	)
)

(define (no-repeats lst) 
	(if (null? lst)
		lst
		(cons 
			(car lst) 
			(no-repeats 
				(my-filter 
					(lambda (t) (not (= t (car lst))))
					(cdr lst)
				)
			)
		)
	)
)
