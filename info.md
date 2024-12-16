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
 20  earliest_credit_line         54231 non-null  object      datetime64 [ns](DONE)
 21  inq_last_6mths               54231 non-null  int64
 22  mths_since_last_delinq       23229 non-null  float64     timedelta64[ns] (DONE)
 23  mths_since_last_record       6181 non-null   float64     timedelta64 [ns] (DONE)
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
 37  next_payment_date            21623 non-null  object       datetime64 [ns] (DONE)
 38  last_credit_pull_date        54224 non-null  object       datetime64 [ns] (DONE)
 39  collections_12_mths_ex_med   54180 non-null  float64       
 40  mths_since_last_major_derog  7499 non-null   float64
 41  policy_code                  54231 non-null  int64
 42  application_type             54231 non-null  object
dtypes: float64(20), int64(8), object(15)


Category for 

- term:
['36 months', '60 months']

- purpose:
['credit_card' 'debt_consolidation' 'home_improvement' 'small_business'
 'renewable_energy' 'major_purchase' 'other' 'moving' 'car' 'medical'
 'house' 'vacation' 'wedding' 'educational']

- Home_ownership: 
['MORTGAGE' 'RENT' 'OWN' 'OTHER' 'NONE']

- Verification_status: 
['Not Verified' 'Source Verified' 'Verified']

- Loan_status: Unique values are (found with print(df['loan_payments].unique()))
['Current' 'Fully Paid' 'Charged Off' 'Late (31-120 days)'
 'In Grace Period' 'Late (16-30 days)' 'Default'
 'Does not meet the credit policy. Status:Fully Paid'
 'Does not meet the credit policy. Status:Charged Off']



To find Null values: self.df.isnull.sum() creates a pandas series which contains the count of null values for each column in the DataFrame. From there we can work out what columns to erase and which ones to impute.

To create a table from the above we do the following: 

        null_cols = null_counts[null_counts > 0] 
         
        if not null_cols.empty:
            null_percentages = (null_cols / len(self.df)) * 100
            null_info = pd.DataFrame({'Null Count': null_cols, 'Null Percentage': null_percentages})
            print(null_info)

From here we see: 

                             Null Count  Null Percentage
funded_amount                      3007         5.544799
term                               4772         8.799395
int_rate                           5169         9.531449
employment_length                  2118         3.905515
mths_since_last_delinq            31002        57.166565 (deliqency = minor crime)
mths_since_last_record            48050        88.602460
last_payment_date                    73         0.134609
next_payment_date                 32608        60.127971
last_credit_pull_date                 7         0.012908
collections_12_mths_ex_med           51         0.094042
mths_since_last_major_derog       46732        86.172116 (derog = Months' since most recent 90-day or worse rating)
(base) 


Aim of this project: gain a comprehensive understanding the loan portfolio data. Need to enable the business to make more informed decisions about approvals, pricing and risk management.

So we can see those that need further exploring in order of highest number of Null values: 

I spoke with Vander after getting confused what to do here and he told me that anything over 80% is definitely drop as there is too much missing data to be useful in later analysis. Even 40% is considered too high, after speaking to Vander and him seeing the columns I was referring to he told me to drop them too. 
Therefore we are going to drop: 
        - 
        - mths_since_last_record: The number of months' since the last public record.
        - mths_since_last_major_derog: Months' since most recent 90-day or worse rating.
        - next_payment_date: Next scheduled payment date.
        - mths_since_last_delinq: The number of months since the last dealing.


These below are low % so will impute using either mean or median:

Use median for: 
- skewed data       
Use mean for: 
- normally distributed 


- int_rate: Annual (APR) interest rate of the loan - impute missing values in this dataset with the median to avoid the influence of outliers and better represent the majority of the data.
- term : number of monthly payments for the loan - use mode for this! 
- funded amount:  The total amount committed to the loan at that point in time - impute missing values in this dataset with the median to avoid the influence of outliers and better represent the majority of the data.
- employment_length: in years - 

If removed the rows of all the null values: 0.09+0.012+0.134+3.9 which would result in MAX of 4.139% of the data being removed is this too much?


