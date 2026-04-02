((label firstatom (lambda (x)
                    (cond ((atom x) x)
                          ('t (firstatom (car x))))))
 '((a b) (c d)))
