
import pandas as pd 

df = pd.read_csv('glassdoor_jobs.csv')

#salary parsing 
df=df[df['Salary Estimate'] != '-1']

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

salary=df['Salary Estimate'].apply(lambda x: x.split('(')[0])
rm_k=salary.apply(lambda x: x.replace('K','').replace('$',''))
rm_txt=rm_k.apply(lambda x: x.lower().replace('employer provided salary:','').replace('per hour',''))


df['min_salary']=rm_txt.apply(lambda x: int(x.split('-')[0]))
df['max_salary']=rm_txt.apply(lambda x: int(x.split('-')[1]))
df['avg_salary']=(df['min_salary']+df['max_salary'])/2
#Company name text only
df['company_txt']=df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3], axis=1)

#state

df['job_state']=df['Location'].apply(lambda x: x.split(',')[1])

df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)
#age of company 
df['age']=df['Founded'].apply(lambda x: x if x<1 else 2022-x)


#parsing of job description
#python
df['python_ln']=df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
 
#r studio 
df['R_ln']=df['Job Description'].apply(lambda x: 1 if 'r studio' or 'r-studio' in x.lower() else 0)
#spark 
df['spark']=df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
#aws 
df['aws']=df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)

#excel

df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

print(df.columns)
df=df.drop(['Unnamed: 0'],axis=1)
df.to_csv('salary_data_cleaned.csv',index=False)

