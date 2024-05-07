from django.shortcuts import render, HttpResponse
from foodOnline import views
from django.contrib import messages
from datetime import datetime, date
import sys
import os
sys.path.insert(1,os.path.abspath("./pyzk"))
from zk import ZK

from vendor.models import Vendor
from django.db import connection
from menu.models import FoodItem


def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True).order_by('-created_at')
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]

    # with connection.cursor() as cursor:
    #     # Execute a raw SQL query
    #    vendors =  cursor.execute("SELECT * FROM vendor_vendor")
    # return HttpResponse(vendors)

    # for number in range(1, 500000):
    #     food_title = 'Food '+str(number) 
    #     slug = 'food -'+ str(number) 
    #     description = 'description - '+str(number)
    #     price = number+100
    #     category_id = 2
    #     vendor_id = 9
    #     FoodItem.objects.create(food_title=food_title, slug=slug, description=description, price=price, category_id=category_id, vendor_id=vendor_id)

    
    
    data = {
        'vendors':vendors
    }
    return render(request, 'home.html', data)


def zktech(request):
    
    conn = None
    zk = ZK('192.168.1.201', port=4370)
    try:
        conn = zk.connect()
        
        print ('Disabling device ...')
        conn.disable_device()
        print ('--- Get User ---')
        # users = conn.get_users()
        attendances = conn.get_attendance()
        start_date = '2024-04-24' 
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = date.today()
        
        # Filter attendances for today's date
        # today_attendances = [attendance for attendance in attendances if attendance.timestamp.date() == end_date]

        

        # Filter attendance records between start_date and end_date
        filtered_attendances = [attendance for attendance in attendances
            if start_date <= attendance.timestamp.date() <= end_date]

        # for attendance in attendances:
        #     print(attendance.user_id, attendance.timestamp)

    
        data = {
            # 'attendance_data':users,
            'attendances':filtered_attendances
        }
        # return HttpResponse(attendances)
        messages.success(request, 'Data fetching from Attendance Device...')
        return render(request, 'zktech.html',data)
    
        # Test Voice: Say Thank You
        conn.test_voice('data in comming')
        # re-enable device after all commands already executed
        conn.enable_device()

    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        if conn:
            conn.disconnect()
    

def custom_404(request, exception):
    return render(request, '404.html', status=404)


