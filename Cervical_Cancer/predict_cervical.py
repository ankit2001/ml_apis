import warnings 
import numpy as np
import pickle

warnings.filterwarnings("ignore")
def predict_cervical(age, no_of_sexual_parteners, age_of_first_intercourse, no_of_pregnancies, smokes, smokes_packs, hormonal_contraceptives, intra_uterine, STDS, any_std, condylomatosis, cervical_condylomatosis, vaginal, vulvo_perineal, syphilis, pelvic, genital, molluscum, AIDS, HIV, hepatitis, HPV, diagnosis, cancer, neoplasis, diagnosis_hpv):
    import os

    pkl_filename = str(os.getcwd()) + "/Cervical_Cancer/pickle_model.pkl"
    with open(pkl_filename, 'rb') as file:
        random_forest_model= pickle.load(file)
    result = random_forest_model.predict(np.array([[age, no_of_sexual_parteners, age_of_first_intercourse, no_of_pregnancies, smokes, smokes_packs, hormonal_contraceptives, intra_uterine, STDS, any_std, condylomatosis, cervical_condylomatosis, vaginal, vulvo_perineal, syphilis, pelvic, genital, molluscum, AIDS, HIV, hepatitis, HPV, diagnosis, cancer, neoplasis, diagnosis_hpv]]))
    if(result >=1):
        return True
    else:
        return False


