### TODO LIST

#### most important feature for now
1. convert language to Bahasa **WIP**
    - translate db value, ig: type of course, gender, etc..
2. registration payment
    - set user account to active if the user completed their registration payment
3. List of Student in table mode.
    - List of Student that didn't tuition payment
        - show the payment status in the current month
        - all months payment status since student has registered
4. List of Teacher in table mode.

5. manipulate data with phone number
    - login with phone number
6. which student has expired tuition payment course..?
7. what if operator add more than 2 course in one payment..?
    - prevent to input multiple student schedule course in one payment
8. expired course time = 4x or 8x per month..?
    - private class = 240 minutes per months | regular class = 960 minutes/month
        - by attedance from teacher..?
        - by time..?
        - count time by when student did the payment..?
    - regular class = 1:30m
9. prevent to input duplicate students schedule
10. prevent to input duplicate teachers schedule
11. add class durations to payment models
----------------------------------------------------------------------------------
12. student Taken courses details
13. total teacher included gender on course_details route
14. disable student account if not active in a time | filter non active user
    - tidak hadir dalam 4x pertemuan di akhir bulan  / tidak membayar dalam 4x pertemuan terakhir
15. werkzeug.routing.BuildError | werkzeug.routing.BuildError: Could not build url for endpoint 'operator.operator_dashboard'. Did you mean 'operator.all_schedules' instead?
16. autobackup to dropbox/google drive..?
17. How we know if a student course or tuition has expired  ..?
18. Kursus yang telah dibayar yang mana yang di ambil jadwal nya..?
19. data dengan umur sekian
20. deploy to a VPS
21. set a domain for the app
22. get current and last login user ip

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
