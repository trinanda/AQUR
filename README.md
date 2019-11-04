### TODO LIST

#### most important feature for now
1. manipulate data with phone number
    - login with phone number
2. update status pembyaran murid jika tidak membayar pada bulan pertama, kedua dan ketiga
    - sp1, sp2, sp3=nonaktivkan
3. deploy to vps for demonstrations

4. List of Student in table mode.
    - List of Student that didn't tuition payment
        - show the payment status in the current month
        - all months payment status since student has registered
5. set payment status to expired if the payment for month has ended. 
    - if that ended, then make a marking to student profile which course has ended.
6. prevent add new schedule if teacher gender is different with student gender
7. prevent add new schedule if teacher email is none
8. List of Teacher in table mode.
9. prevent to input duplicate students schedule
10. prevent to input duplicate teachers schedule
----------------------------------------------------------------------------------
11. delete profile photo feature
12. student Taken courses details
13. total teacher included gender on course_details route
14. werkzeug.routing.BuildError | werkzeug.routing.BuildError: Could not build url for endpoint 'operator.operator_dashboard'. Did you mean 'operator.all_schedules' instead?
15. autobackup to dropbox/google drive..?
16. data dengan umur sekian
17. deploy to a VPS
18. set a domain for the app
29. get current and last login user ip
20. batasi umur

##### Important feature
1. Murid
    - Lihat profile
    
2. Guru
    - Absensi kehadiran murid
    - Lihat profile (himself and their students)
    
3. Operator
    - Broadcast jika ada kajian dan even lainnya
    - Data keuangan
        - spp murid    
        - gaji guru
            - bonus guru
    - graph (registrasi murid, keuangan)
    - absensi murid dan guru


This app use this nicely boilerplate
https://github.com/hack4impact/flask-base
