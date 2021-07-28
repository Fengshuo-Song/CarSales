from cars.models import download_delete  # 删除文件
from cars.models import Car, CarImage
from mycar.settings import DEBUG
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import fields
from django.contrib import messages
from django import http
import os
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count
import datetime
from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect
from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from django.db.models.fields import DecimalField
from typing import Reversible
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from cars.forms import CarForm, RatingForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.core.files.images import ImageFile
from .models import Car
from django.db.models import Q
import random


@login_required
def product_list(request):
    print('request.user.username:', request.user.username)
    car_list = Car.objects.all()

    return render(request,
                  'cars/list.html',
                  {'car_list': car_list, 'user': request.user.username})


@login_required
def product_detail(request, vin):
    car = get_object_or_404(Car, VIN=vin)
    photos = CarImage.objects.filter(car=car)

    print(len(car.comments.all()))
    print(len(car.ratings.all()))
    ratings = car.ratings.filter()
    comments = car.comments.filter(active=True)
    new_rating = None
    new_comment = None
    
    if request.method == 'POST' and "Rate" in request.POST:
        rating_form = RatingForm(data=request.POST)
        if rating_form.is_valid():
            new_rating = rating_form.save(commit=False)
            new_rating.car = car
            new_rating.save()
    else:
        rating_form = RatingForm()

    if request.method == 'POST' and "Add comment" in request.POST:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.car = car
            new_comment.save()
    else:
        comment_form = CommentForm()

    def avg(obj):
        n = len(obj)
        sumc = sump = sums = sumr = 0
        for item in obj:
            sumc += int(item.comfort_rating)
            sump += int(item.performance_rating)
            sums += int(item.safety_rating)
            sumr += int(item.reliability_rating)
        return round(sumc / n + 0.05, 1), round(sump / n + 0.05, 1), round(sums / n + 0.05, 1), round(sumr / n + 0.05, 1), round((sumc+sump+sums+sumr) / n / 4 + 0.05, 1)

    if len(ratings.all()) == 0:
        c = p = s = r = o = "NA"
    else:
        c, p, s, r, o = avg(ratings.all())

    return render(request,
                  'cars/detail.html',
                  {'car': car, 'photos': photos,
                  'c': c, 'p': p, 's': s, 'r': r, 'o': o,
                  'new_rating': new_rating,
                  'rating_form': rating_form,
                  'comments': comments,
                  'new_comment': new_comment,
                  'comment_form': comment_form})

def CarReset(request):
    Car.objects.all().delete()
    all_cars = ["Porsche#Cayenne#TurboS E-Hybrid#2020#180000.00#suv#hybrid#example/Cayenne#Metallic White#Black & Mojave#4.0L V8 32V GDI DOHC Twin Turbo#AWD#670#4.0#V8#663#5#15#19",
                "Dodge#Challenger#SRT#2020#50000.00#car#gas#example/Challenger#Mango#Red#6.2L V8 16V MPFI OHV Supercharged#RWD#707#6.2#V8#656#5#13#22",
                "Toyota#Corolla#S#2013#8000.00#car#gas#example/Corolla#Red#Black#1.8L I4 16V MPFI DOHC#FWD#130#1.8#I4#120#5#25#35",
                "Ford#F-150#XLT#2018#30000.00#truck#gas#example/F150#Grey#Black#--#4*4#350#4.0#V8#500#5#14#19",
                "Mercedes Benz#G63 AMG##2019#80000.00#suv#gas#example/GWagon#Metallic Black#Black#4.0L V8 32V GDI DOHC Twin Turbo#AWD#577#4.0#V8#627#5#14#19",
                "Lexus#LC#Structural Blue Edition#2019#150000.00#car#gas#example/LC#Blue#White#--#RWD#471#5.0#V8#398#2#15#19",
                "Mazda#Mazda3 Hatchback#2.5 Turbo#2020#34000.00#car#hybrid#example/Mazda3#Red#Black#2.5L I4 16V GDI DOHC#AWD#250#2.5#I4#220#5#28#36",
                "Toyota#Mirai#Limited#2021#63000.00#car#other#example/Mirai#Metallic White#Black & Mojave#--#RWD#182#0##221#5#67#64",
                "Cadilac#Escalade#Plantinum#2021#120000.00#suv#gas#example/Escalade#Dark Mocha Metallic#Gideon #6.2L V8 16V GDI OHV#AWD#420#6.2#V8#600#7#14#18",
                "Chrysler#Pacifica Hybrid##2021#48000.00#van#hybrid#example/Pacifica#Metallic White#Black & Mojave#--#AWD#260#3.6#V6#235#5#82#82",
                "Dodge#Ram#Long Horn Edition#2020#50000.00#truck#diesel#example/Ram#Metallic White#Black & Mojave#3.0L V6 Diesel#4*4#260#3.0#V6#480#5#21#30",
                "Toyota#4Runner##2002#3000.00#suv#gas#example/Runner#--#--#3.4L V6 32V GDI#AWD#183#3.4#V6#213#5#16#19",
                "Chevrolet#Suburban#LTZ#2015#40000.00#suv#gas#example/Suburban#White#--#6.2L V8 16V GDI OHV#AWD#355#6.2#V8#383#7#16#23",
                "Porsche#Taycan#Turbo#2021#170000.00#car#electric#example/Taycan#Metallic White#Black & Mojave#--#AWD#680#0#--#627#5#15#19",
                "Audi#TT#RS#2020#78000.00#car#gas#example/TT#Blue#Black#--#AWD#394#2.5#L5#354#4#20#30", ]
    de = ["Special 2.49 available financing on our new 2021 *Cayenne Turbo S E-Hybrid**.* For the best deal call or email General Manager William Winstel or any of our Porsche Certified Sales Consultants today! 513-851-5900, bill@porscheofkingsautomall.com.",
          "Clean CARFAX. CARFAX One-Owner. New Price! *Routine Maintenance Up To Date*, *Nonsmoker*, Navigation, Sunroof, Automatic Headlights, Smartphone App Integration, Black Fuel Filler Door, Black Grille w/Bezel, Blacktop Package, Challenger Blacktop Grille Badge, Gloss Black I/P Cluster Trim Rings, GPS N avigation, GT Black Grille Badge, Navigation System, Quick Order Package 2EL GT, Rear Black Spoiler, Satin Black Dodge Tail Lamp Badge, Wheels: 20 x 8.0 Black Noise Painted. 2D Coupe 2020 19/30 City/Highway MPG 2020 Dodge Challenger GT Dodge GT 3.6L V6 24V VVT 8-Speed Automatic Challenger RWD Granite Crystal Metallic Clearcoat 19/30 City/Highway MPG\n Come find out how we earned a Five-Star Award for Outstanding Service in 2016! Browse our online inventory, and feel free to give us a call at any of our three locations.",
          "Introducing the Love Your Car Guarantee from CarMax! Now you can take your time with a 24-hour test drive and a 30-day/1500-mile money back guarantee to be sure its the right car for you. See carmax.com for details. At CarMax, finding the right car is easy. You can shop online, get pre-approved for financing, and receive a trade-in offer all from the comfort of home. Then, when its time to buy, you can choose curbside pickup at your local CarMax or home delivery in select markets. And we stand behind every used car we sell with a 90-Day/4,000-Mile (whichever comes first) Limited Warranty. See store for details. Price assumes final purchase will be made in AZ, and excludes tax, title, tags and $199 CarMax processing fee (not required by law). Some fees are location specific and may change if you transfer this vehicle to a different CarMax store. Certain vehicles may have unrepaired safety recalls. Check nhtsa.gov/recalls to learn if this vehicle has an unrepaired safety recall. Inventory shown here is updated every 24 hours.",
          "Up to date VA inspection, Multi Point inspection completed, F-150 XLT, 4D SuperCrew, 5.0L V8, 10-Speed Automatic, 4WD, Shadow Black, Black w/Unique Sport Cloth 40/Console/40 Front-Seats or Unique Sport Cloth 40/Console/40 Front-Seats, 10-Way Power Driver & Passenger Seats, 2-Bar Style Grille w/2 Min or Bars Painted Dark, 4.2 Productivity Screen in Instrument Cluster, 4x4 FX4 Off-Road Bodyside Decal, ABS brakes, Accent-Color Step Bars, Air Conditioning, Auto-Dimming Rear-View Mirror, Black Running Boards, Body-Color Door & Tailgate Handles, Body-Color Front & Rear Bumpers, Body-Color Surround Grille w/Black Mesh Insert, Box Side Decal, Box Side Decals, Class IV Trailer Hitch Receiver, Cloth 40/20/40 Front Seat, Compass, Electronic Locking w/3.73 Axle Ratio, Electronic Stability Control, Equipment Group 302A Luxury, Exterior parking camera rear: With Dynamic Hitch Assist, Fixed Backlight w/Privacy Glass, Front fog lights, Fully automatic headlights, FX4 Off-Road Package, Heated Front Seats, Hill Descent Control, Illuminated entry, Integrated Trailer Brake Controller, Leather-Wrapped Steering Wheel, LED Sideview Mirror Spotlights, Low tire pressure warning, Manual-Folding Heated Pwr Glass Trailer Tow Mirror, Off-Road Tuned Front Shock Absorbers, Power Glass Heated Sideview Mirrors, Power-Adjustable Pedals, Radio: Single-CD/SiriusXM w/7 Speakers, Rear Under-Seat Storage, Rear Window Defroster, Remote keyless entry, Remote Start System, Reverse Sensing System, Security system, Speed control, SYNC, SYNC 3, Telescoping steering wheel, Tilt steering wheel, Traction control, Unique Bodyside & Hood Decals, Wheel Well Liner (Pre-Installed), Wheels: 20 Unique Premium Tarnished Dark Painted, XLT Special Edition Package, XLT Sport Appearance Package. TO KEEP YOU SAFE, WE DELIVER! BUY ONLINE-TEXT-EMAIL-CHAT-PHONE AND WE WILL DELIVER YOUR NEXT VEHICLE TO YOUR DOOR! FROM OUR SALES FLOOR TO YOUR DOOR! IT'S THAT EASY! Ford Blue Certified Details: * Vehicle History * Transferab\n Blake has been dealing quality automobiles for 35 YEARS!. We know what customers want. Now Blake is proud to offer new & used vehicles to you! Always with the best financing options and pricing. Price excludes tax, title, and tags and PROCESSING FEE of $699.00. Same then. Same now. Test drive today! Call us toll-free 757-569-9756 or stop by and ask for Gerry Givens!",
          "****NAVIGATION*****BLUETOOTH*****BACK-UP SYSTEM**** **ORIGINAL MSRP $177,100**EXCLUSIVE INTERIOR PACKAGE:AMG EXCLUSIVE NAPPA LEATHER WITHDIAMOND QUILT STITCHING,NAPPA LEATHER DASHBOARD,AMG BADGING INHEADREST AND FLOOR MATS,ACTIVE MULTICONTOUR FORNT SEATS WITHMASSAGE, AND RAPID HEATING/VENTILATED SEA TS $7,200**22INCH FORGED AMG CROSS-SPOKE WHEELS FINISHED IN BLACK $4,450**AMG CARBON FIBER TRIM $3,700**DESIGNO GRAPHITE METALLIC $2,300**AMG NIGHT PACKAGE: EXTERIOR MIRRORS,SPARE WHEEL COVER RING,AND TRIM ELEMENTS IN BUMPER PAINTED IN OBSIDIAN BLACK,BLACK BRUSH GUARD,AMG SPECIFIC RADIATOR GRILLEIN GUNMETAL GREY,TINTED FRONT INDICATOR LIGHTS AND TAILLIGHTS $1,950**PLEASE CALL 7045357100 TO VERIFY AVAILABILITY** SAVE YOUR CASH ASK ABOUT OUR SUPER LOW RATE FINANCING**EXTENDED TERMS AVAILABLE TO QUALIFIED CLIENTELE**",
          "The custom version of the handsome Lexus LC 500 coupe was part of the Lexus display in Las Vegas, at the annual SEMA show, a first in the company's new Inspiration Series and something of a rarity at the trade show. The distinction for the Structural Blue edition of the LC 500-one of six Lexus custo ms at SEMA 2018-is that it actually found its way into showrooms in 2018 as a very limited edition-just 100 cars. While the vivid blue metallic paint is hard to miss, the source of the inspiration may be a little harder to perceive. Inspired by Marvel comics According to Lexus, this first limited edition Lexus owes its inspiration to King T'Challa, a character in Marvel's Black Panther series set in the mythical country of Wakanda. Exactly what relationship his majesty T'Challa has to a slinky 471-horsepower sports coupe is a little hard to see, but may be clear to Marvel faithful. Other elements of the LC 500 Inspiration edition include 21-inch forged alloy wheels, carbon fiber scuff plates, and a white leather interior, making a stark contrast with the blue exterior finish. As a footnote, Lexus notes that the Structural Blue finish was inspired by the Morpho butterfly, and that the paint goes through an eight-month development process. This Launch Edition is virtually brand new with only 160 miles. This is a true collector car that will only go up in value. Call us before this one gets away! We have fantastic finance options for this beautiful LC 500 as well as nationwide shipping. Trade-ins welcome, call now........................ Air Conditioning, Climate Control, Dual Zone Climate Control, Power Steering, Power Windows, Power Mirrors, Leather Steering Wheel, Power Drivers Seat, Memory Seat Position, Clock, Tachometer, Homelink System, Telescoping Steering Wheel, Steering Wheel Radio Controls, Sunroof, Moonroof, Driver Airbag, Passenger Airbag, Side Airbags, Security System, Rear Defogger, Intermittent Wipers, AM/FM, Anti-Theft, Leather Interior Surface, Blu ...\n OC Autosource takes pride hand selecting every vehicle we offer for sale. Every employee works commission free to make your automotive purchase a comfortable and friendly experience. We strive to offer the lowest interest rates available and will pay above market value for your trade vehicle. Zero down financing on approved credit available. We offer nationwide financing and shipping every day.",
          "Scores 33 Highway MPG and 25 City MPG! This Mazda Mazda3 Sedan delivers a Intercooled Turbo Regular Unleaded I-4 2.5 L/152 engine powering this Automatic transmission. SOUL RED METALLIC PAINT CHARGE, SOUL RED CRYSTAL METALLIC, PREMIUM PLUS PACKAGE.*This Mazda Mazda3 Sedan Comes Equipped with These O ptions *BLACK, LEATHER SEAT TRIM, Window Grid And Roof Mount Antenna, Wheels: 18 x 7J Black Finish Alloy, Valet Function, Trunk Rear Cargo Access, Trip Computer, Torsion Beam Rear Suspension w/Coil Springs, Tires: P215/45R18 M+S, Tire Specific Low Tire Pressure Warning, Systems Monitor.* Visit Us Today *A short visit to Cutter Buick GMC Mazda Waipahu located at 94-245 Farrington Highway, Waipahu, HI 96797 can get you a dependable Mazda3 Sedan today!",
          "01l5/Heavy Metal 2021 Toyota Mirai Limited RWD 1-Speed Automatic AC Synchronous Electric Motor 67/64 City/Highway MPG\n At Toyota Santa Monica, a member of the LAcarGUY Auto Group, sets the bar for the way vehicles are purchased. The difference begins with a caring and experienced staff. Toyota Santa Monica is a state-of-the art facility with award winning sales team and service department. Call today to schedule your personal tour 888-453-0895 and discover why we are one of the fastest growing dealers in LA.",
          "Visit Classic Cadillac in Atlanta on Roswell Road! See this and our entire New inventory at www.classiccadillacatlanta.com or call us now at 770-394-9100! MSRP may not reflect the final retail price based on incentives, finance offers, and availability. See Dealer for details. Classic Cadillac of At lanta is pumped up to offer this great 2021 Cadillac Escalade Sport in Black Raven, Beautifully equipped with Driver Assist Tech Package (Adaptive Cruise Control, Air Ride Adaptive Suspension, Automatic Seat Belt Tightening, Enhanced Automatic Emergency Braking, Illuminating Front & Rear Sill Plates, Reverse Automatic Braking, and Soft Closing Front & Rear Doors), Heavy-Duty Trailering Package (2-Speed Active Transfer Case, Extra Capacity Cooling System, Trailer Tire Pressure Monitoring System, Trailering Assist Guidelines, and Wired Auxiliary Trailer Camera (LPO)), Preferred Equipment Group 1SH (Air Ionizer, AKG Studio Reference 36-Speaker Audio System, Body-Color Door Handles, Door Lock & Latch Shields, Electronic Limited-Slip Differential, Enhanced Automatic Parking Assist, Floor Console w/Covered Storage, Glass Breakage Sensor, Hitch Guidance w/Hitch View, Integrated Trailer Brake Controller, In-Vehicle Trailering System App, Lane Keep Assist w/Lane Departure Warning, Platinum Interior Trim, Power Panoramic Tilt-Sliding Sunroof, Rear Camera Mirror, Rear Camera Mirror Washer, Rear Cross Traffic Alert, Rear Seat Entertainment System, Reconfigurable Full-Color Head-Up Display, Running Board Assist Steps, Theft-Deterrent Alarm System, Trailer Side Blind Zone Alert, Vehicle I\nClassic Cadillac has been Atlanta's #1 dealer since 2009 because we make it fast, easy, and fun to purchase a vehicle. Call and talk to our Certified Internet Managers and experience the quality care and service you deserve!",
          "Plus TAVT, Tag, and Title. Must present ad or mention that you saw this price on our website to receive quoted price. Subject to prior sale. Includes Dealer Doc Fee.\n WE RESERVE THE RIGHT TO REFUSE TO HONOR ANY INCORRECT INTERNET PRICES AS WE CANNOT ACCOUNT FOR THE OCCASIONAL HUMAN OR TECHNICAL ERROR.",
          "Certified. Certification Program Details: 3 month/3000 Miles Certified Warranty *ONE OWNER, *CLEAN CARFAX, *Certified Pre-Owned 3 month/ 3,000 Mile Warranty, *BACKUP CAMERA, *BLUETOOTH, HANDS-FREE, *NAVIGATION/NAV/GPS, *SUNROOF/MOONROOF, *LEATHER, *REMOTE START, *HEATED SEATS, *COOLED SEATS, *MEMORY SEATS, *FIXED RUNNING BOARDS, *ULTRA SONIC REAR PARKING ASSIST, *TOW PACKAGE, *NON-SMOKER, *WOOD GRAIN INTERIOR*, *HEATED 2ND ROW SEATING, *BEDLINER, *ALLOY WHEELS, *PUSH TO START. Awards: * NACTOY 2013 North American Truck of the Year If there is any information or extra photos you need that you don't see listed, we will walk out to the vehicle and text them directly to you! JUST ASK!\n FREE DELIVERY to NC,SC, & GA! Tax and Tags not included in vehicle prices shown and must be paid by the purchaser. Five hundred and ninety dollar closing fee is included in the sales price. Customer must mention this advertisement to receive advertised price.",
          "2002 Toyota 4Runner SR5 ONLY 95K Original Miles Check out this awesome Toyota 4Runners. Last year for the sought after 3rd Generation body style. In generation three, the 4Runner became its own thing. It got an all-new body sitting on a chassis that wasn't shared with a pickup. Engines grew to 3.4-l iter V-6 upgrade. Off-road capability remained a focus, but numerous changes helped make it a nicer road car. Body styling was smoothed, the wheelbase was lengthened, and the interior was thoroughly revised to improve space and ergonomics. This one has power windows, power locks, rear cargo mat, cargo cover, AM/FM/CD Player, and so much to offer in interior cabin comfort and the ability to get you around safely in all kinds off driving conditions. Won't find that many out there with low miles and everyone knows these last several 100Ks of miles so it driving life is just getting started. Comes with MO State inspections, limited warranty, and 30 day temp tag. Call (636) 465-6732 for availability and appointments Michael Thomas Motor Co 521 Little Hills Industrial Blvd. St. Charles, MO 63301 www.mtmotorcars.com Located two buildings up the hill from Fast Lane Classic Cars (636) 465-6732 Call ahead for availability and appointments www.mtmotorcars.com We sell SUV, Diesel Trucks, Luxury, Sports Car, Van, Cargo Van, Heavy Duty, Super Duty, Crew Cab, Quad Cab, Convertible, Coupe, 4X4, Truck, SUV, Pickup Truck, Heavy Duty, Super Duty, Sedan, Van, Mini Van, Cargo Vans, Work Vans, F-150, F-250, F-350, and much more!!",
          "This 2015 Chevrolet Suburban 4dr LTZ features a 6.2L 8 CYLINDER 8cyl Flex Fuel engine. It is equipped with a 6 Speed Automatic transmission. The vehicle is Sable Metallic with a Cocoa/Dune Leather interior. It is offered with a full factory warranty. - One owner, Non-Smoker, Dealer inspection, All s cheduled maintenance, Dealer maintained, Have service records, Have original manuals, This Chevrolet is in Excellent overall exterior condition, Excellent overall interior condition, Leather seats - Air Conditioning, Climate Control, Power Steering, Power Windows, Power Door Locks, Power Mirrors, Power Drivers Seat, Rear Air Conditioning, Tilt Steering Wheel, Steering Wheel Radio Controls, Driver Airbag, Passenger Airbag, Side Airbags, Keyless Entry, Security System, ABS Brakes, Traction Control, Dynamic Stability, Rear Defogger, Fog Lights, Intermittent Wipers, AM/FM, Leather Interior Surface, Satellite; Sentry Key; Active Seatbelts 3rd Row Seating, Carpeted Floor Mats, Cup Holders, Daytime Running Lights, Heated Mirrors, HID Headlamps, Navigation System, OnStar, Parking Sensors, Power Adjustable Pedals, Power Lift Gate, Premium Sound, Rear AC Seats, Remote Trunk Lid, Reverse Camera, Roll Stability Control, Running Boards, Side Curtain Airbags, Tire Pressure Monitor - Contact General Dealership at 404-454-0000 or sales@automaxatlanta.com for more information. - OVER 60+ PICS ONLINE ON OUR WEBSITE @ WWW.AUTOMAXATLANTA.COM -\n Automax Atlanta is where Quality, Value, and Excellence meet for an outstanding Pre-Owned Automobile Purchasing and Ownership Experience. We consistently provide clients with top-notch customer service, high-quality products, and exceeding levels of general satisfaction.",
          "Burmester High-End Surround Sound-System,Performance Package,Premium Package,Wheels: 21 Taycan Exclusive Design,Porsche Innodrive W/Adaptive Cruise Control (Acc),Atacama Beige/Basalt Blk; Olea Club Leather Seat Trim,Interior Trim In Matte Carbon Fiber,Front Massage Seat Function W/Seat Ventilation, Illuminated Door-Sill Guards In Matte Carbon Fiber,Passenger Display,Mobile Charger Connect,Interior Accents In Exterior Color,Advanced 4-Zone Climate Control,Heated Steering Wheel W/Matte Carbon Fiber Trim,Lane Change Assist (Lca),Exterior Package In High Gloss Black,Porsche Surface Coated Brakes (Pscb),Seat Belts In Graphite Blue,Led-Matrix Design Headlights In Glacier Blue,Vehicle Keys Painted W/1 Key Pouch In Leather,Leather Seats,Navigation System,Center Console Armrest W/Model Designation,Window Trim In High Gloss Black,Power Folding Exterior Mirrors,Taycan Turbo Logo On Doors In Silver,Lane Keeping Assist,Keyless Start,Bluetooth Connection,Rear Spoiler,Cooled Front Seat(S),All Wheel Drive,Electric Logo On Front Doors In High Gloss Silver,Gentian Blue Metallic",
          "Recent Arrival! 2021 Audi TT RS 2.5T 20/30 City/Highway MPG Audi Atlanta is proud to be the only Magna Society dealership in Georgia! Our inventory moves extremely quickly. PLEASE BE SURE TO SECURE YOUR APPOINTMENT. All vehicles are subject to sale at any time. As a courtesy to our clients, a partia l payment and signed agreement will secure an appropriate window of time to allow for travel to inspect and accept the vehicle.\n Please call our Internet Department at 877-646-7944 for more information on this great offer!", ]
    for index, item in enumerate(all_cars):
        il = item.split("#")
        newcar = Car.objects.create()
        newcar.brand = il[0]
        newcar.model = il[1]
        if il[2] != "":
            newcar.trim = il[2]
        newcar.year = int(il[3])
        import decimal
        newcar.price = decimal.Decimal(il[4])
        newcar.style = il[5]
        newcar.fuel_type = il[6]
        newcar.mileage = (2022-int(il[3])) * \
            8000 + random.randrange(-1000, 1000)
        newcar.VIN = "Brand"+str(index)
        newcar.owner_name = "owner_name"+str(random.randrange(-1000, 1000))
        newcar.description = de[index]

        newcar.exterior_color = il[8]
        newcar.interior_color = il[9]
        newcar.engine = il[10]
        newcar.drivetrain = il[11]
        newcar.horsepower = int(il[12])
        newcar.displacement = float(il[13])
        newcar.cylinder = il[14]
        newcar.torque = int(il[15])
        newcar.seating = int(il[16])
        newcar.city_mpg = int(il[17])
        newcar.hwy_mpg = int(il[18])

        ls = os.listdir("media/"+il[7])
        for i in ls:
            if i[0] == "1":
                path = "media/"+il[7]+"/"+i
                break
        newcar.image = ImageFile(open(path, "rb"))
        newcar.save()

        for i in ls:
            path = "media/"+il[7]+"/"+i
            newimg = CarImage.objects.create(car=newcar)
            newimg.image = ImageFile(open(path, "rb"))
            newimg.save()

    next_url = reverse('cars:car_list')
    return redirect(next_url)


def CarClear(request):
    Car.objects.all().delete()
    next_url = reverse('cars:car_list')
    return redirect(next_url)


class CarListView(ListView):
    model = Car
    paginate_by = 5


class CarDetailView(DetailView):
    model = Car


class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy('cars:car_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '「{}」has been created successfully!'.format(form.instance))
        messages.success(
            self.request, '「{}」has been created successfully!'.format(self.request.POST))
        messages.success(
            self.request, '「{}」has been created successfully!'.format(self.request.FILES))

        # form.instance.pk

        return result

    def form_invalid(self, form):
        print("form is invalid")
        return http.HttpResponse("form is invalid.. this is just an HttpResponse object")


class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm

    success_url = reverse_lazy('cars:car_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '「{}」has been updated successfully!'.format(form.instance))
        messages.success(
            self.request, '「{}」has been updated successfully!'.format(self.request.POST))
        messages.success(
            self.request, '「{}」has been updated successfully!'.format(self.request.FILES))

        return result


class CarDeleteView(DeleteView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy('cars:car_list')

    def delete(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            # print("================= cancel =======================")
            next_url = reverse('cars:car_list')
            return redirect(next_url)

        else:
            # instance = download.objects.get(id=1)
            # download_delete(instance)
            result = super().delete(request, *args, **kwargs)
            messages.success(
                self.request, '「{}」was deleted successfully!'.format(self.object))
            messages.success(
                self.request, '「{}」has been updated successfully!'.format(self.request.POST))
            messages.success(
                self.request, '「{}」has been updated successfully!'.format(self.request.FILES))
            return result


def gallery_view(request):
    photos = CarImage.objects.all()
    return render(request,
                  'cars/gallery.html',
                  {'photos': photos})


@ login_required(login_url='login')
def addPhoto(request, vin):
    car = get_object_or_404(Car, VIN=vin)

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        for image in images:
            photo = CarImage.objects.create(
                car=car,
                image=image,
            )

        next_url = reverse('cars:car_list')
        return redirect(next_url)

    context = {'car': car}
    return render(request, 'cars/add.html', context)


def search_view(request):
    if request.method == "POST":
        searched = request.POST['searched']
        if searched == "":
            return render(request,
                          'cars/search.html',
                          {})
        results = Car.objects.filter(
            Q(brand__contains=searched) | Q(model__contains=searched))
        return render(request,
                      'cars/search.html',
                      {'searched': searched, 'results': results})
    return render(request,
                  'cars/search.html',
                  {})


class RateView(UpdateView):

    model = Car
    form_class = RatingForm

    # success_url = self.get_object_url()

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, 'Thank you for your rating「{}」!'.format(form.instance))

        messages.success(
            self.request, '「{}」has been updated successfully!'.format(self.request.POST))
        messages.success(
            self.request, '「{}」has been updated successfully!'.format(self.request.FILES))

        return result
