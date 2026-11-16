# Run with base R. All observations below are invented.
counts <- c(4, 8, 17, 31, 50, 69, 83, 92, 96)
train <- data.frame(
  hours = rep(1:9, each = 100),
  passed = unlist(lapply(counts, function(k) c(rep(1, k), rep(0, 100-k))))
)
fit <- glm(passed ~ hours, data = train, family = binomial(link = "logit"))

new <- data.frame(hours = c(3, 6, 7))
p <- predict(fit, newdata = new, type = "response")
print(coef(fit))
print(data.frame(hours = new$hours, p = p, class = as.integer(p >= 0.5)))
print(exp(coef(fit)["hours"]))  # odds multiplier per extra hour

# Separate, invented test observations; not used to fit or choose the threshold.
test_counts <- c(1, 2, 4, 6, 10, 14, 16, 18, 19)
test <- data.frame(
  hours = rep(1:9, each = 20),
  passed = unlist(lapply(test_counts, function(k) c(rep(1, k), rep(0, 20-k))))
)
test_p <- predict(fit, newdata = test, type = "response")
q <- pmin(pmax(test_p, 1e-12), 1-1e-12)
print(-mean(test$passed * log(q) + (1-test$passed) * log1p(-q)))
