import math

def maxVal(lst): # position of max value in the input list
	val = lst[0][1]
	arg = lst[0][0]
	
	pos = 0
	
	for i in range(1, len(lst)):
		if (lst[i][1] > val): # in case of multiple maximum values returns the first one
			val = lst[i][1]
			pos = i
	
	return pos

def createList():
	file = open("gauss-input.txt", 'r')
	s = file.readlines()
	for i in range(len(s)):
		s[i] = s[i].split()
		for j in range(len(s[i])):
			s[i][j] = float(s[i][j])
	return s

def main():

	print("\n\n-----GAUSS FITTER-----\n")

	inp = createList()
	pos = maxVal(inp)
	
	arg = inp[pos][0]
	val = inp[pos][1]
	darg = None
	if (pos == 0): # maximum value at the beginning
		print("type 1")
		darg = inp[1][0] - inp[0][0]
		vald = inp[1][1]
	elif (pos == len(inp)): # maximum value at the end
		print("type 2")
		darg = inp[-1][0] - inp[-2][0]
		vald = inp[-2][1]
	elif ((inp[pos+1][0] - inp[pos][0] > inp[pos][0] - inp[pos-1][0]) and not (inp[pos+1][1] == inp[pos][1])): # right-hand argument is more distant and does not have another maximum value
		print("type 3")
		darg = inp[pos+1][0] - inp[pos][0]
		vald = inp[pos+1][1]
	else: # left-hand argument is more (or equally) distant or the right-hand argument's value is another maximum
		print("type 4")
		darg = inp[pos][0] - inp[pos-1][0]
		vald = inp[pos-1][1]
	
	if (vald == 0): vald = val/1000 # a small non-zero value, to enable further computetions
	
	med = arg
	
	var = darg**2/(2*(math.log(val/vald)))
	k = val*math.sqrt(2*math.pi*var)
	
	dmed = var
	dvar = 10
	dk = 10
	
	
	step = 0
	
	endFLAG = False
	
	while (True):
		
		step += 1
		if (step > 1): break
	
		print("Optimization step", step)		
		print("med = {0:8.5f} ± {1:.2e}\tvar = {2:8.5f} ± {3:.2e}\tk = {4:8.5f} ± {5:.2e}".format(med, dmed, var, dvar, k, dk))
	#	print()
	
		# compute needed values
		thisdiff = 0
		leftdiff = 0
		rightdiff = 0
		updiff = 0
		downdiff = 0
		behinddiff = 0
		forwarddiff = 0
		
		for x in inp:
			thisdiff += (x[1] - k*(1/math.sqrt(2*math.pi*var))*math.exp(-((x[0]-med)**2/(2*var))))**2
			leftdiff += (x[1] - k*(1/math.sqrt(2*math.pi*var))*math.exp(-((x[0]-(med-dmed))**2/(2*var))))**2
			rightdiff += (x[1] - k*(1/math.sqrt(2*math.pi*var))*math.exp(-((x[0]-(med+dmed))**2/(2*var))))**2
			updiff += (x[1] - k*(1/math.sqrt(2*math.pi*(var/(1+dvar))))*math.exp(-((x[0]-med)**2/(2*(var/(1+dvar))))))**2
			downdiff += (x[1] - k*(1/math.sqrt(2*math.pi*(var*(1+dvar))))*math.exp(-((x[0]-med)**2/(2*(var*(1+dvar))))))**2
			behinddiff += (x[1] - (k/(1+dk))*(1/math.sqrt(2*math.pi*var))*math.exp(-((x[0]-med)**2/(2*var))))**2
			forwarddiff += (x[1] - (k*(1+dk))*(1/math.sqrt(2*math.pi*var))*math.exp(-((x[0]-med)**2/(2*var))))**2
			
		print(thisdiff, leftdiff, rightdiff, updiff, downdiff, behinddiff, forwarddiff)

		# slide if needed
		if (leftdiff < thisdiff):
			med -= dmed
			continue
		if (rightdiff < thisdiff):
			med += dmed
			continue
		if (updiff < thisdiff):
			var /= (1+dvar)
			continue
		if (downdiff < thisdiff):
			var *= (1+dvar)
			continue
		if (behinddiff < thisdiff):
			k /= (1+dk)
			continue
		if (forwarddiff < thisdiff):
			k *= (1+dk)
			continue

		# tighten values
		if (max(leftdiff + rightdiff, updiff + downdiff, behinddiff + forwarddiff) == leftdiff + rightdiff):
			dmed /= 1.5
			dvar /= 1.2
			dk /= 1.2
		elif (max(leftdiff + rightdiff, updiff + downdiff, behinddiff + forwarddiff) == updiff + downdiff):
			dmed /= 1.2
			dvar /= 1.5
			dk /= 1.2
		else:
			dmed /= 1.2
			dvar /= 1.2
			dk /= 1.5
		
		# finish if converged
		if (leftdiff + rightdiff + updiff + downdiff + behinddiff + forwarddiff - 6*thisdiff < 10**(-30)): # very small difference - converged
			break
		if (dmed < 10**(-30) and dvar < 10**(-30) and dk < 10**(-30)): # extremely small uncertainties - converged
			break
			
	print("OPTIMIZATION COMPLETED:")
	print("med = {0:8.5f} ± {1:.2e}\tvar = {2:8.5f} ± {3:.2e}\tk = {4:8.5f} ± {5:.2e}".format(med, dmed, var, dvar, k, dk))

if __name__ == "__main__": main()
