### TODO LIST

#### most important feature for now
1.  set starting course date on schedule
    - set payment status to expired automatically after pay_at pass the current date
    - if status payment == expired transfer payment data to fixed_payment table
2. List of Student in table mode.
    - List of Student that didn't tuition payment
        - show the payment status in the current month
        - all months payment status since student has registered
3. set payment status to expired if the payment for month has ended. 
    - if that ended, then make a marking to student profile which course has ended.
4. prevent add new schedule if teacher gender is different with student gender
5. prevent add new schedule if teacher email is none

6. List of Teacher in table mode.
7. manipulate data with phone number
    - login with phone number
8. which student has expired tuition payment course..?
10. expired course time = 4x or 8x per month..?
    - private class = 240 minutes per months | regular class = 960 minutes/month
        - by attedance from teacher..?
        - by time..?
        - count time by when student did the payment..?
    - regular class = 1:30m
11. prevent to input duplicate students schedule
12. prevent to input duplicate teachers schedule
----------------------------------------------------------------------------------
13. fix "Please input correct image format" when change user profile data
14. student Taken courses details
15. total teacher included gender on course_details route
16. disable student account if not active in a time | filter non active user
    - tidak hadir dalam 4x pertemuan di akhir bulan  / tidak membayar dalam 4x pertemuan terakhir
17. werkzeug.routing.BuildError | werkzeug.routing.BuildError: Could not build url for endpoint 'operator.operator_dashboard'. Did you mean 'operator.all_schedules' instead?
18. autobackup to dropbox/google drive..?
19. How we know if a student course or tuition has expired  ..?
20. data dengan umur sekian
21. deploy to a VPS
22. set a domain for the app
23. get current and last login user ip

##### TODO | 2 -
1. batasi umur
2. filter non active user
3. tidak hadir dalam 4x pertemuan di akhir bulan  / tidak membayar dalam 4x pertemuan terakhir

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
