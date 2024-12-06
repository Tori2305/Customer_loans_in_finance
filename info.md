#   Column                       Non-Null Count  Dtype      Needs changing?     
---  ------                       --------------  -----
 0   id                           54231 non-null  int64             
 1   member_id                    54231 non-null  int64
 2   loan_amount                  54231 non-null  int64         
 3   funded_amount                51224 non-null  float64       
 4   funded_amount_inv            54231 non-null  float64       
 5   term                         49459 non-null  object        
 6   int_rate                     49062 non-null  float64       
 7   instalment                   54231 non-null  float64       
 8   grade                        54231 non-null  object        string (DONE)
 9   sub_grade                    54231 non-null  object     
 10  employment_length            52113 non-null  object        
 11  home_ownership               54231 non-null  object        category (DONE)
 12  annual_inc                   54231 non-null  float64       
 13  verification_status          54231 non-null  object        category (DONE)
 14  issue_date                   54231 non-null  object        datetime64[ns] (DONE BUT WILL NEED TO REMOVE DAY AS WILL BE INCORRECT)
 15  loan_status                  54231 non-null  object        category (DONE)
 16  payment_plan                 54231 non-null  object
 17  purpose                      54231 non-null  object        string (DONE)
 18  dti                          54231 non-null  float64
 19  delinq_2yrs                  54231 non-null  int64
 20  earliest_credit_line         54231 non-null  object        datetime64 [ns](DONE)
 21  inq_last_6mths               54231 non-null  int64
 22  mths_since_last_delinq       23229 non-null  float64       timedelta64[ns] (DONE)
 23  mths_since_last_record       6181 non-null   float64       timedelta64 [ns] (DONE)
 24  open_accounts                54231 non-null  int64
 25  total_accounts               54231 non-null  int64
 26  out_prncp                    54231 non-null  float64
 27  out_prncp_inv                54231 non-null  float64
 28  total_payment                54231 non-null  float64
 29  total_payment_inv            54231 non-null  float64
 30  total_rec_prncp              54231 non-null  float64
 31  total_rec_int                54231 non-null  float64
 32  total_rec_late_fee           54231 non-null  float64
 33  recoveries                   54231 non-null  float64       
 34  collection_recovery_fee      54231 non-null  float64
 35  last_payment_date            54158 non-null  object        datetime64[ns] (DONE)
 36  last_payment_amount          54231 non-null  float64
 37  next_payment_date            21623 non-null  object        datetime64 [ns] (DONE)
 38  last_credit_pull_date        54224 non-null  object        datetime64 [ns] (DONE)
 39  collections_12_mths_ex_med   54180 non-null  float64       
 40  mths_since_last_major_derog  7499 non-null   float64
 41  policy_code                  54231 non-null  int64
 42  application_type             54231 non-null  object
dtypes: float64(20), int64(8), object(15)


Updated version: 



df.issue_date= df['issue_date'].astype('datetime64')

print(df['verification_status'].info())



Category for 

- Home_ownership: 
['MORTGAGE' 'RENT' 'OWN' 'OTHER' 'NONE']

- Verification_status: 
['Not Verified' 'Source Verified' 'Verified']

- Loan_status: Unique values are (found with print(df['loan_payments].unique()))
['Current' 'Fully Paid' 'Charged Off' 'Late (31-120 days)'
 'In Grace Period' 'Late (16-30 days)' 'Default'
 'Does not meet the credit policy. Status:Fully Paid'
 'Does not meet the credit policy. Status:Charged Off']




We know that there should be 54231 rows so if any of the Non-Null are less than this then we need to explore these. df.isna().mean*100 provided me with the following answer: 

(54231, 43)                  Null values (%)        Explore?
id                              0.000000
member_id                       0.000000
loan_amount                     0.000000
funded_amount                   5.544799                Y
funded_amount_inv               0.000000
term                            8.799395                Y    
int_rate                        9.531449                Y
instalment                      0.000000
grade                           0.000000
sub_grade                       0.000000
employment_length               3.905515                Y
home_ownership                  0.000000
annual_inc                      0.000000
verification_status             0.000000
issue_date                      0.000000
loan_status                     0.000000
payment_plan                    0.000000
purpose                         0.000000
dti                             0.000000
delinq_2yrs                     0.000000
earliest_credit_line            0.000000
inq_last_6mths                  0.000000
mths_since_last_delinq         57.166565                Y
mths_since_last_record         88.602460                Y
open_accounts                   0.000000
total_accounts                  0.000000
out_prncp                       0.000000
out_prncp_inv                   0.000000
total_payment                   0.000000
total_payment_inv               0.000000
total_rec_prncp                 0.000000
total_rec_int                   0.000000
total_rec_late_fee              0.000000
recoveries                      0.000000
collection_recovery_fee         0.000000
last_payment_date               0.134609                Y
last_payment_amount             0.000000
next_payment_date              60.127971                Y
last_credit_pull_date           0.012908                Y
collections_12_mths_ex_med      0.094042                Y
mths_since_last_major_derog    86.172116                Y    
policy_code                     0.000000
application_type                0.000000
dtype: float64

Exploration needed for the following in order of highest number of Null values: 
- mths_since_last_record: The number of months' since the last public record
- mths_since_last_major_derog: Months' since most recent 90-day or worse rating
- next_payment_date: Next scheduled payment date
- mths_since_last_dealing: The number of months since the last dealing.
- int_rate: Annual (APR) interest rate of the loan.
- term : number of monthly payments for the loan.
- funded amount:  The total amount committed to the loan at that point in time
- employment_length: in years



