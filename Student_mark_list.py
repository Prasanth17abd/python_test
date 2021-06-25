

#Part 2

filename = r'C:\Users\Prasanth M Praveen\Downloads\Student_marks_list.csv'
with open(filename, 'r') as f:
    file = f.read()
    file = [row.split(',') for row in file.splitlines()]
    
# For Each subject toppers    
# Approach with O(n*subjects) time complexity and O(subjects) space complexity
topper = {}
for col_ind, col in enumerate(file[0][1:]):
    mx = 0
    for row in file[1:]:
        if int(row[col_ind+1])>mx:
            topper[col]=row[0]
            mx = int(row[col_ind+1])
print(topper)

# Top 3 Steudents in the class,based on their marks in all subjects
# Approach time complexity - O(n) and space complexity O(n)
all_marks = [sum(map(int, row[1:]))for row in file[1:]]
all_marks = list(zip(all_marks, [f[0] for f in file[1:]]))
all_marks.sort(key=lambda x: -x[0])
all_marks[:3]    
    