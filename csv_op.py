import csv

def reader_cvs(cvs_filename):
    reader = csv.reader(file(cvs_filename, 'rb'))
    for line in reader:
        print line

def writer_cvs(cvs_filename):
    writer = csv.writer(file(cvs_filename, 'wb'))
    writer.writerow(['Column1', 'Column2', 'Column3'])
    lines = [range(3) for i in range(5)]
    for line in lines:
        writer.writerow(line)

if __name__ == '__main__':
    writer_cvs('in.csv')
    reader_cvs('in.csv')

def save_result_to_csv(cvs_filename, results, spec_data=''):
    writer = csv.writer(file(cvs_filename, 'wb'))

    for result in results:
        shop_name = result['shop_name']
        comments = result['comments']
        for comment in comments:
            if spec_data == '' or spec_data == comment['date']:
                writer.writerow( [shop_name, comment['username'], comment['date'], comment['comment'], comment['star'] ])
