
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Voter
from collections import Counter
from . import db   
from flask_login import login_user, login_required, logout_user, current_user
import math
import random 
from math import gcd
import hashlib
from sqlalchemy import or_


auth= Blueprint('auth', __name__)
def gcd(a,b):
    return a if b==0 else gcd(b,a%b)
def ext_eu(a,b):
    if(a<b):
        a,b=b,a
    s=0;s1=1;t=1;t1=0;rem=b;divid=a
    while(rem>0):
        quot=divid//rem; rem1=rem
        divid,rem=rem,divid-quot*rem
        s1,s=s,s1-quot*s
        t1,t=t,t1-quot*t
    return [rem1,s1%a,t1%a]
def modinverse(a,b):
    return (ext_eu(a,b)[2])

set_of_x_values=[]
number=1151
selected_root=1131
def initialising_phase(number):
    o = 1
    roots = []
    z = 0
    r = number - 1
    while z < 20:
        k = math.pow(r, o)
        k = k % number

        while k > 1:
            o += 1
            k *= r
            k = k % number
        if o == (number - 1):
            roots.append(r)
            z += 1
        o = 1
        r -= 1
    roots= list(reversed(roots))
    selected_root = random.choice(roots)
    #selected_root=1131
    #x = random.randint(3, number - 3)

    #x=709
    #x = random.randint(3, number - 3)
    
    count=0
    while count<100:
        #while():
        x = random.randint(3, number - 3)
        if (gcd(x, number - 1) == 1):
            count+=1
           # x = random.randint(3, number - 3)
            set_of_x_values.append(x)
            
    x=random.choice(set_of_x_values)
    
       
        
        #if gcd(x, number - 1) == 1:
        
       
    print("secret number ",x)
    y = pow(selected_root, x) % number
    #t=()
    public_key=(y,selected_root,number)
    print(public_key)
    return public_key,x
def random_coprime(n):
    while True:
        #k = random.randint(2, n-2)
        k=1067
    
        if math.gcd(k, n-1) == 1:
            print("Random chose prime, kdash",k)
            return k
def generate_relatively_prime_numbers(p):
        a=499
        b=501
        c=1021
        while True:
            a = random.randint(2, p-1)
            b = random.randint(2, p-1)
            c = random.randint(2, p-1)
                



            if a != b and b != c and a != c and gcd(a, p-1) == 1 and gcd(b, p-1) == 1 and gcd(c, p-1) == 1:
                print("value of a",a)
                print("value of b",b)
                print("value of c",c)
                return a, b, c 
              

                      
def blinding_phase_signer(pkey):
    y=pkey[0]
    g=pkey[1]
    p=pkey[2]
    K=random_coprime(p)
    rdash=pow(g,K,p)%p
    print("value of rdash",rdash)
    return rdash,K
def blinding_phase_requester(m):
    a,b,c=generate_relatively_prime_numbers(p)
    print("This is the value of c ",c)
    
    rdashhed=blinding_phase_signer(pub_key)[0]
    r1 = (pow(rdashhed, a, p) * pow(y, b, p) * pow(g, c, p)) % p
    print("r value",r1)
    print("hello")

    h_m = int(hashlib.sha1(str(m).encode()).hexdigest(), 16)
    #h_m=50
    a_inv = modinverse(a, p-1)
    
    print("inverse of a",a_inv)
    addedhash=c+h_m+r1
    a_inverse_multiplied=a_inv*addedhash
    m_blinded=(a_inverse_multiplied-rdashhed)%(p-1)
    #m_blinded = ((a_inv*((c+h_m+r1)))-rdashhed)%(p-1)
    
   
    return m_blinded,a,b,r1,h_m
def signing_phase(m_blinded):
    
    print("Secret key value",secret_key_x)
    rdashed,kay=blinding_phase_signer(pub_key)
    
    x_inv = modinverse(secret_key_x, p-1)
    #x_inv=1069
    print("x inverse",x_inv)
    temp=0
    temp=(temp+(m_blinded + rdashed))%(p-1)
    temp=(temp+kay)%(p-1)
    s1=(x_inv*temp)%(p-1)
   # s1 =( x_inv * (kay + ((m_blinded + rdashed)%(p-1))%(p-1)) % (p-1))%(p-1)
    return s1
def unblinding_phase(s1,a,b,m,rrr):
    
    s=(((a*s1)%(p-1))+b)%(p-1)
    print("value of s",s)

    message_signature_pair=(m,rrr,s)
    return message_signature_pair
def verifying_phase(message_signature_pair):
    v1 = pow(y, message_signature_pair[2], p)
    print("s value from message signature pair",message_signature_pair[2])
    h_m = int(hashlib.sha1(str(message_signature_pair[0]).encode()).hexdigest(), 16)
    print("this is v1",v1)
    V1="The verification from message signature pair is "+str(v1)

    v2 = (mod_exp(g, message_signature_pair[1], p) * mod_exp(g, h_m, p) * (message_signature_pair[1]%p))%p 
    
    V2="The verification from message signature pair is "+str(v2)
    return v1,v2

def mod_exp(base, exp, mod):
    result = 1
    base = base % mod

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod

        exp = exp // 2
        base = (base * base) % mod

    return result
pub_key,secret_key_x=initialising_phase(1151)
print(pub_key)
y=pub_key[0]
g=pub_key[1]
p=1151

@auth.route('/send_to_verifier/<int:voter_id>', methods=['POST'])
def send_to_verifier(voter_id):
    messagesigpair,blinded_msg = process_vote(voter_id)

    if request.form.get('send_to_verifier') == 'true':
        vv1, vv2 = verifying_phase(messagesigpair)
        
        
        voter = Voter.query.get(voter_id)
        
        if voter.already_voted==False:
            voter.v1 = vv1
            voter.v2 = vv2
            print("hello")
            db.session.commit()
        else:
            voter.v2=vv2 
            db.session.commit()   
        
        voter.request_sent="verifying"
        db.session.commit()
        
        
               

        flash("Sent to verifier!", category='success')
        

        
        
        

    return redirect(url_for('auth.signers_dashboard'))
@auth.route('/retrival_verifier/',methods=['GET','POST'])
def retrival_verifier():
    

    return url_for('auth.verifiers_dashboard')
@auth.route('/approve/<int:voter_id>',methods=['GET','POST'])
@login_required
def approve(voter_id):
    voter=Voter.query.get(voter_id)
    voter.request_sent="approved"
    db.session.commit()
    verifying_voters = Voter.query.filter_by(request_sent="verifying").all()
    flash("It has been approved!")
    return render_template('verifiers_dashboard.html', verifying_voters=verifying_voters)

     
@auth.route('/reject/<int:voter_id>',methods=['GET','POST'])
@login_required
def reject(voter_id):
    voter=Voter.query.get(voter_id)
    voter.request_sent="rejected"
    db.session.commit()
    flash("It has been rejected!")
    verifying_voters = Voter.query.filter_by(request_sent="verifying").all()


    return render_template('verifiers_dashboard.html',verifying_voters=verifying_voters)
@auth.route('/pie_chart')
@login_required
def pie_chart():
    # Query the database to get non-null values of m
    

    voters_with_m = Voter.query.filter(
    or_(Voter.request_sent == 'approved', Voter.already_voted == True)
).all()


    # Count the occurrences of each value of m
    party_mapping = {
        241: 'Party A',
        342: 'Party B',
        493: 'Party C',
        914: 'Party D'
        # Add more mappings as needed
    }

    # Replace each m value with the corresponding party name
    m_values_party = [party_mapping.get(voter.msg, 'Unknown') for voter in voters_with_m]

    # Count the occurrences of each party name
    party_count = Counter(m_values_party)

    # Prepare data for the pie chart
    labels = list(party_count.keys())
    values = list(party_count.values())

    return render_template('piechart.html', labels=labels, values=values) 
@auth.route ('/signer',methods=['POST','GET'])
def login_signer():
    name = request.form.get('name')
    password=request.form.get('password')
    voter = Voter.query.filter_by(name=name).first()
    if name == 'Signer' and password == 'Signer123':
        login_user(voter)
        voters_with_request_sent = Voter.query.filter_by(role="voter", request_sent="Pending").all()
        print(voters_with_request_sent)
        return render_template('signers_dashboard.html',voters_without_roles=voters_with_request_sent)
        # Authentication successful, redirect or perform further actions
        
    else:
        
        # Authentication failed, handle accordingly (e.g., redirect to login page with an error message)
        flash("Incorrect credentials!", category='error4')
        
        return render_template('login.html') 
@auth.route ('/verifier',methods=['POST','GET'])
def verifier_login():
    name = request.form.get('name')
    print(name)
    password=request.form.get('password')
    voter=Voter.query.filter_by(name=name).first()
    
    
    if voter and voter.password == password:
        login_user(voter)
        verifying_voters = Voter.query.filter_by(request_sent="verifying").all()
        
        print(verifying_voters)
        return render_template('verifiers_dashboard.html', verifying_voters=verifying_voters)
    else:
        flash("Incorrect credentials!", category='error4')
        return redirect(url_for('auth.login'))
    
      
     
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        voter_id = request.form.get('voter_id')
        print(voter_id)
        name = request.form.get('name')
        print(name)
        password = request.form.get('password')
        print(password)
        aadhar_id = request.form.get('aadhar_id')
        print(aadhar_id)

        voter = Voter.query.filter_by(name=name).first()
        
            
        if voter is not None:
            # Check if the password matches
            
            if voter.password == password and voter.aadhar_id==aadhar_id and voter.voter_id==voter_id:
                login_user(voter)
                if voter.request_sent=="approved":
                    voter.already_voted=True
                    voter.request_sent="No"
                    db.session.commit()
                    return render_template("votingmessage.html",sign='approved')
                if voter.request_sent=="rejected":
                    voter.already_voted=True
                    voter.request_sent="No"
                    db.session.commit()
                    return render_template("votingmessage.html",sign='rejected')
               
                return redirect(url_for('auth.voter_dashboard'))

           
                
            else:
                flash('Incorrect credentials, try again.', category='error4')
    return render_template('login.html')



        
       
@auth.route('/logout')
def logout():
    
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/voter_dashboard')
@login_required
def voter_dashboard():
    voter = current_user  # Replace with your logic to get the current voter

    return render_template('voter_dashboard.html', voter=voter)
    
#@auth.route('/process_vote/<int: voter_id>')
def process_vote(voterid):
    
    voter=Voter.query.get(voterid)
    if voter.already_voted==True:
        selected_choice=random.randint(4,354)
    else:
         selected_choice=voter.msg

    
    message_blind,a,b,rrr,h_m=blinding_phase_requester(selected_choice)

        
        
    sdashed=signing_phase(message_blind)
    m_s_pair=unblinding_phase(sdashed,a,b,selected_choice,rrr)
    return m_s_pair,message_blind
        
    
        
@auth.route('/thankyou/<int:voterid>',methods=['POST','GET'])
@login_required
def thankyou(voterid):
    selected_choice = request.form.get('exampleRadios')
    
    voter=Voter.query.get(voterid)
    
    if voter.already_voted==True:
        current_user.request_sent = "Pending"
        db.session.commit()
        return render_template('thankyou.html')
        

    if voter.request_sent=="No":
        voter.msg=selected_choice
        voter.request_sent = "Pending"
        db.session.commit()
    flash("Thank you for voting")
    return render_template('thankyou.html')

@auth.route('/verifiers_dashboard')
@login_required
def verifiers_dashboard():
    
        
    # Retrieve vv1 and vv2 from the session
    

    return render_template('verifiers_dashboard.html')
    
        

            
@auth.route('/get_blinded_messages', methods=['POST'])
@login_required
def get_blinded_messages():
    if current_user.name != "Signer":
        flash("You are not allowed to authorize this action", category='danger')
    else:
        voters_with_request_sent = Voter.query.filter_by(role="voter", request_sent="Pending").all()

        for voter in voters_with_request_sent:
            if not voter.already_voted:
                blinded_msg = getblindedmsg(voter.id)
                

    return redirect(url_for('auth.signers_dashboard'))

# Your existing code ...

# Modify your existing getblindedmsg function
def getblindedmsg(voterid):
    voter = Voter.query.get(voterid)
    messagesigpair, blinded_msg = process_vote(voterid)

    voter.blinded_msg = blinded_msg
    voter.msg = messagesigpair[0]
    voter.r = messagesigpair[1]
    voter.s = messagesigpair[2]
    db.session.commit()

    return blinded_msg


def getblindedmsg(voterid):
    voter = Voter.query.get(voterid)
    messagesigpair, blinded_msg = process_vote(voterid)

    voter.blinded_msg = blinded_msg
    voter.msg = messagesigpair[0]
    voter.r = messagesigpair[1]
    voter.s = messagesigpair[2]
    db.session.commit()

    return blinded_msg  # Add this line to return blinded_msg

@auth.route('/signers_dashboard')
@login_required
def signers_dashboard():
    if current_user.name != "Signer":
        flash("You are not allowed to authorize this page", category='danger')
        return redirect(url_for('auth.login'))  # Redirect to login page or another page

    # Fetch voters with pending requests
    voters_with_request_sent = Voter.query.filter_by(role="voter", request_sent="Pending").all()

    # Iterate through voters and update blinded messages
    

    return render_template('signers_dashboard.html', voters_without_roles=voters_with_request_sent)


   





    

    

    

