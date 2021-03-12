import joblib
import os
loaded_model = joblib.load(str(os.getcwd()) + '/Pcos/model.pkl')
import warnings
warnings.filterwarnings("ignore")
def g(s):
    if(s=="YES"):
        return 1
    if(s=="NO"):
        return 0
    if s=="Yes":
        return 1
    if s=="No":
        return 0
    if s=="abc":
        return 2
    return 0

def predict_PCOS(age, Chin, Cheeks, Lips, Breast, Arms, Thigh, Exercise, Eat, PCOS, BMI, Weight, Period, Concieve, Skin, Hairthin, Patch, Tired, Mood, Can, City):
    y_inputtest = [[age,Chin,Cheeks,Lips,Breast,Arms,Thigh,Exercise,Eat,PCOS,BMI,Weight,Period,Concieve,Skin,Hairthin,Patch,Tired,Mood,Can,City]]
    for i in range(1,13):
        y_inputtest[0][-i]=g(y_inputtest[0][-i])
    output = (loaded_model.predict(y_inputtest))
    if output[0] == True:
        return True
    else:
        return False

#print(predict_PCOS(8, 4, 3, 4, 2, 2, 1, 3, 3, "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"))
