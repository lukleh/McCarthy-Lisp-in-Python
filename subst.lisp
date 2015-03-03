
(eval '((label subst (lambda (x1 y1 z1)
                                        (cond ((atom z1)
                                               (cond ((eq z1 y1) x1)
                                                     ('t z1)))
                                              ('t (cons (subst x1 y1 (car z1))
                                                        (subst x1 y1 (cdr z1)))))))
         x2 y2 z2)

      '((x2 m) (y2 b) (z2 (a b (a b c) d))))