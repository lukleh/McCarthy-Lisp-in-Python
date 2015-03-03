
(label null (lambda (x)
      (eq x '())))


(label and (lambda (x y)
  (cond (x (cond (y 't) ('t '())))
        ('t '()))))


(label not (lambda (x)
  (cond (x '())
        ('t 't))))


(label append (lambda (x y)
  (cond ((null x) y)
        ('t (cons (car x) (append (cdr x) y))))))


(label pair (lambda (x y)
  (cond ((and (null x) (null y)) '())
        ((and (not (atom x)) (not (atom y)))
         (cons (cons (car x) (cons (car y) '()))
               (pair (cdr x) (cdr y)))))))


(label assoc (lambda (x y)
  (cond ((eq (car (car y)) x) (car (cdr (car y))))
        ('t (assoc x (cdr y))))))


(label eval (lambda (e a)
  (cond
    ((atom e) (assoc e a))
    ((atom (car e))
     (cond
       ((eq (car e) 'quote) (car (cdr e)))
       ((eq (car e) 'atom)  (atom   (eval (car (cdr e)) a)))
       ((eq (car e) 'eq)    (eq     (eval (car (cdr e)) a)
                                    (eval (car (cdr (cdr e))) a)))
       ((eq (car e) 'car)   (car    (eval (car (cdr e)) a)))
       ((eq (car e) 'cdr)   (cdr    (eval (car (cdr e)) a)))
       ((eq (car e) 'cons)  (cons   (eval (car (cdr e)) a)
                                    (eval (car (cdr (cdr e))) a)))
       ((eq (car e) 'cond)  (evcon (cdr e) a))
       ('t (eval (cons (assoc (car e) a)
                       (cdr e))
                  a))))
    ((eq (car (car e)) 'label)
     (eval (cons (car (cdr (cdr (car e)))) (cdr e))
           (cons (cons (car (cdr (car e))) (cons (car e) '())) a)))
    ((eq (car (car e)) 'lambda)
     (eval (car (cdr (cdr (car e))))
           (append (pair (car (cdr (car e))) (evlis (cdr e) a))
                     a))))))

(label evcon (lambda (c a)
  (cond ((eval (car (car c)) a)
         (eval (car (cdr (car c))) a))
        ('t (evcon (cdr c) a)))))

(label evlis (lambda (m a)
  (cond ((null m) '())
        ('t (cons (eval  (car m) a)
                  (evlis (cdr m) a))))))