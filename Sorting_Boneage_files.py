# Originally, this dataseat contains a grade which shows the speed of patient's growth and 0 means the speed is normal.
# So I extract the data and excel data which labeled as 0.
# At the same time, I split with gender.

# --------- Sorting Label file ---------

excel = pd.read_excel('/Volumes/Seagate/Boneage/Label_0only_sonya.xlsx', dtype={'Test Number': str, 'Chronological Age': np.int32})



#excel['Sex'] = excel['Sex'].map(lambda x: True if x == 'M' else False)

#print(excel.sample(10))



# --------- Load image file ---------

BASE_PATH = '/Volumes/Seagate/Boneage/'

ORIGIN_PATH = os.path.join(BASE_PATH, 'Bone_Age_Session1_2nd_origin/Bone age session 1')

TARGET_PATH = os.path.join(BASE_PATH, 'Session1_Sort')



list_patients = os.listdir(ORIGIN_PATH)



for patient in list_patients:

    PATIENT_PATH = os.path.join(ORIGIN_PATH, patient)

    list_tests = os.listdir(PATIENT_PATH)



    for test in list_tests:

        TEST_PATH = os.path.join(PATIENT_PATH, test)

        # --------- match test number and excel ---------

        if test in excel['Test Number'].values:  # match test number

            matched_excel = excel[excel['Test Number'] == test]

            if int(matched_excel.Images) == 1:

                list_cases = os.listdir(TEST_PATH)

                CASE_PATH = os.path.join(TEST_PATH, list_cases[0])  # cause there is only one case

                list_images = os.listdir(CASE_PATH)

                if len(list_images) == 1:  # validate whether only 1 image is exist

                    IMG_ORIGIN_PATH = os.path.join(CASE_PATH, list_images[0])

                    img_name = matched_excel['Sex'].item() + '_' + str(matched_excel['Chronological Age'].item()) + '_' + str(matched_excel['Test Number'].item()) + '.dcm'

                    print(img_name)

                    if matched_excel['Sex'].item() == 'F':

                        IMG_TARGET_PATH = os.path.join(TARGET_PATH, 'Normal', 'Female', img_name)

                        #print(IMG_TARGET_PATH)

                        shutil.copy(IMG_ORIGIN_PATH, IMG_TARGET_PATH)

                    else:

                        IMG_TARGET_PATH = os.path.join(TARGET_PATH, 'Normal', 'Male', img_name)

                        shutil.copy(IMG_ORIGIN_PATH, IMG_TARGET_PATH)

                else:

                    IMG_TARGET_PATH = os.path.join(TARGET_PATH, 'ETC', test)

                    print("there are more than one image in dir: {}".format(TEST_PATH))

                    shutil.copytree(TEST_PATH, IMG_TARGET_PATH)

            else:

                IMG_TARGET_PATH = os.path.join(TARGET_PATH, 'ETC', test)

                print("there are more than one dir: {}".format(TEST_PATH))

                shutil.copytree(TEST_PATH, IMG_TARGET_PATH)



        else:

            IMG_TARGET_PATH = os.path.join(TARGET_PATH, 'Abnormal', test)

            print("origin: {} \ntarget: {}".format(TEST_PATH, IMG_TARGET_PATH))

            shutil.copytree(TEST_PATH, IMG_TARGET_PATH)
