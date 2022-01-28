library(graphics)
library(nortest)

#Створення нормального розподілу
x <- seq(-100, 100, by = 0.01)
y <- rnorm(x)

is_sigmas = FALSE
is_ms = FALSE

a1 <- mean(y) #середнє
a2 <- median(y) #медіана
a3 <- density(y)$x[which.max(density(y)$y)] #мода

#перевірка на поавило 3 м
a_list <- c(a1, a2, a3)
a_cr <- a2 + 0.5
a_cr2 <- a2 - 0.5

c <- 0
for(i in 1:(length(a_list))){
  if (a_list[i] > a_cr2 && a_list[i] < a_cr) {c <- c + 1}
  else {}
}

d_y = dnorm(y) #розподіл плотності
plot(y,d_y)

sig1 <- sd(y)#знаходимо значення сігм
sig2 <- sd(y)*2
sig3 <- sd(y)*3
percents <- c(99.72, 95.44, 68.26)

#перевірка на поавило сігм
counting <- function(sig) {
  counter <- 0
  for(i in 1:(length(x))){
    if (y[i] > -sig && y[i] < sig) {
      counter = counter + 1
    }
  }
  return(counter)
}

c1 <- counting(sig1)
c2 <- counting(sig2)
c3 <- counting(sig3)
c_list <- c(c3, c2, c1)

counter2 <- 0
for(i in 1:(length(c_list))){
  cr1 <- percents[i] - 3
  cr2 <- percents[i] + 3
  c_pers <- (c_list[i]*100)/length(y)
  if (c_pers > cr1 || c_pers < cr2) {
    counter2 = counter2 + 1
  }
}

if (counter2 == 3) {
  cat("Правило трьох сігм виконується")
  is_sigmas = TRUE
}

if (c == 3) {
  cat("Правило трьох М виконується")
  is_ms = TRUE
}

if (is_sigmas && is_ms) {cat("Розподіл нормальний")}

print(counter)