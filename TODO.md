### TODO LIST

#### most important feature for now
1. all-teachers view | jumlah murid yang diaajar
2. fix static error on account.register views
3. if user is authenticated, redirect it to the it role homepage.
4. all-schedules
    schedule i18&l10
5. change login background-image
6. re-check SCHEDULER_JOB_DEFAULTS
7. think about taking_courses on student-profile, do we need it..?
8. what if operator add space after email_or phone_number form..?
9. prevent to input duplicate teachers schedule at the same time
----------------------------------------------------------------------------------
10. get current and last login user ip | do this feature when the students feature available
11. if payment status == warning-3, disable user account | do this feature when the students feature available

#### ask when the meething time
1. Re-check all feature before ask Ustadz Faidil for the meeting time
2. how much students do the tuition payment in a day..?
3. delete profile photo feature, should we do this..?
4. thinking about check_schedule feature..?, should we enable the feature..?

#### hope will be more simplified process when using this app
##### pros:
1. students payment status, "completed, installment, pending, sp1, sp2, sp3"
2. more accessible data
    - we have the necessary data about students and teachers
        - name, gender, address, phone_mumber, email, etc..
            - we can contact the students easily, eg: when we have kajian schedule
3. save
    - paper usage
    - electricity
    - ink usage
    - time, etc..
4. be more productive
5. graph monitoring
    - courses
    - teachers
    - students

##### cons:
1. server cost about 80.000 idr each month
2. domain cost about 25.000 each years

##### future development
1. Murid
    - Lihat profile
2. Guru
    - Absensi kehadiran murid
    - Lihat profile (himself and their students)
3. Operator
    - Broadcast jika ada kajian dan even lainnya
    - Data keuangan
        - gaji guru
            - bonus guru
    - graph (registrasi murid, keuangan)
    - absensi murid dan guru


This app use this nicely boilerplate
https://github.com/hack4impact/flask-base
