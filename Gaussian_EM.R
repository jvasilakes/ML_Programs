# Runs through a 2 gaussian mixture model for a 1 dimensional
# data set. Assumes two clusters. 

get_weights <- function(main_probs, supp_probs, main_mix_param, supp_mix_param) {
	ws = c()
	for (i in seq(1, length(main_probs))) {
		ws[i] = (main_probs[i]*main_mix_param) /
		        ((main_probs[i]*main_mix_param) +
			 (supp_probs[i]*supp_mix_param))
	}
	return(ws)
}

# Initial values

# The set to be clustered.
set <- c(-9, -8, -7, -6, -5, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9)

# Initial means for each gaussian.
a.mean <- -10
b.mean <- -9 

# Initial variances for each gaussian.
a.var <- 1
b.var <- 1

# Initial mixture paramters for each gaussian.
a.mix = 0.5
b.mix = 0.5

print("== Starting Values ==")
print(sprintf("a.mean: %g", a.mean))
print(sprintf("a.var: %g", a.var))
print(sprintf("a.mix: %g", a.mix))
print(sprintf("b.mean: %g", b.mean))
print(sprintf("b.var: %g", b.var))
print(sprintf("b.mix: %g", b.mix))

# Print the initial gaussians.
x <- seq(set[1], set[length(set)], by=0.1)
a.y <- dnorm(x, mean=a.mean, sd=sqrt(a.var))
b.y <- dnorm(x, mean=b.mean, sd=sqrt(b.var))

height = max(c(a.y, b.y))
plot(NULL, xlim=c(-10, 10), ylim=c(0, height), xlab="", ylab="", main="Initial Gaussians")
points(set, rep(0, length(set)))
lines(x, a.y, col="red")
lines(x, b.y, col="blue")

readline()

print("++++++++++++++++++++++")
print("Starting Mixture Model")
print("++++++++++++++++++++++")

# ----------------


# Calculate the new parameters at each iteration and print
# a graph of the gaussians over the data points.
# Process ceases when means stop changing. 
repeat{
	aprobs <- dnorm(set, mean=a.mean, sd=sqrt(a.var))
	bprobs <- dnorm(set, mean=b.mean, sd=sqrt(b.var))

	a.weights = get_weights(aprobs, bprobs, a.mix, b.mix)
	b.weights = get_weights(bprobs, aprobs, b.mix, a.mix)

	old.a.mean = a.mean
	old.b.mean = b.mean
	a.mean <- sum(a.weights*set) / sum(a.weights)
	b.mean <- sum(b.weights*set) / sum(b.weights)

	# Stop when the means stop changing.
	if (a.mean - old.a.mean == 0 & b.mean - old.b.mean == 0) {
		break
	}

	a.var <- sum(a.weights * (set-a.mean)**2) / sum(a.weights)
	b.var <- sum(b.weights * (set-b.mean)**2) / sum(b.weights)

	a.mix = sum(a.weights) / length(set)
	b.mix = sum(b.weights) / length(set)

	print(sprintf("a.mean: %g", a.mean))
	print(sprintf("a.var: %g", a.var))
	print(sprintf("a.mix: %g", a.mix))
	print(sprintf("mean a.weights: %g", mean(a.weights)))
	print(sprintf("b.mean: %g", b.mean))
	print(sprintf("b.var: %g", b.var))
	print(sprintf("b.mix: %g", b.mix))
	print(sprintf("mean b.weights: %g", mean(b.weights)))
	print("===========")

	Sys.sleep(0.5)

	x <- seq(set[1], set[length(set)], by=0.1)
	a.y <- dnorm(x, mean=a.mean, sd=sqrt(a.var))
	b.y <- dnorm(x, mean=b.mean, sd=sqrt(b.var))

	height = max(c(a.y, b.y))
	plot(NULL, xlim=c(-10, 10), ylim=c(0, height), xlab="", ylab="")
	points(set, rep(0, length(set)))
	lines(x, a.y, col="red")
	lines(x, b.y, col="blue")
}
