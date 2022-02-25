sex = 'female'
Pclass = 3
Fare = 7.56
survived = 0

if sex =='male':
    survived=0
elif sex == 'female' and Pclass == 3 and Fare > 20:
    survived=0
else:
    survived=1

print(survived)

