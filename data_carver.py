try:
    import os
    import sys
    import hashlib
    import threading
    from prettytable import PrettyTable
except:
    print('Please install required modules before running the code....')

global hash_obj,file_details

#The directory in which the carved files will be stored ( Pls change as per requirement, since its hard-coded )
dir_path='/root/Desktop/data_carver/Thiagarajan/'
hash_path='/root/Desktop/data_carver/Thiagarajan/hash.txt'
hash_obj=hashlib.md5()
file_details={}

def output_table():
    table=PrettyTable()
    filename=[]
    size=[]
    offsets=[]
    hashes=[]
   
    for i in list(file_details.keys()):
        x=file_details[i]
        filename.append(i)
        size.append(x[0])
        offsets.append(x[1])
        hashes.append(x[2])

    table.add_column('File_name',filename)
    table.add_column('Size',size)
    table.add_column('Offsets',offsets)
    table.add_column('Md5 Hashes',hashes)
    print(table)
        
        
def data_carver(file,file_ext):
    sof=[]
    eof=[]
    if file_ext=='.pdf':
        sof_num=4
        eof_num=4
        file_type='PDF'
        sof_byte1=b'\x25'
        sof_byte2=[b'\x25\x50\x44\x46']
        eof_byte1=b'\x25'
        eof_byte2=b'\x25\x45\x4f\x46'

    elif file_ext=='.png':
        sof_num=8
        eof_num=8
        file_type='PNG'
        sof_byte1=b'\x89'
        sof_byte2=[b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a']
        eof_byte1=b'\x49'
        eof_byte2=b'\x49\x45\x4e\x44\xae\x42\x60\x82'

    elif file_ext=='.jpg':
        sof_num=4
        eof_num=2
        file_type='JPG'
        sof_byte1=b'\xff'
        sof_byte2=[b'\xff\xd8\xff\xe0',b'\xff\xd8\xff\xe1',b'\xff\xd8\xff\xe2',b'\xff\xd8\xff\xe8']
        eof_byte1=b'\xff'
        eof_byte2=b'\xff\xd9'
        
        
        
        
    
    dd=open(file,'rb')
    data=dd.read()
    dd.close()

   
    
    print('\nSearching for SOF and EOF of ',file_type,' files...')

    for x in sof_byte2:
        a=0
        eof=[]
        with open(file,'rb') as f:
            byte=f.read(1)
            while byte:
                byte=f.read(1)
                a=a+1
               
                if byte==sof_byte1:
                    byte2=data[a:a+sof_num]

                    if byte2==x:
                       
                        sof.append(hex(a))

          
                if byte==eof_byte1:
                    byte2=data[a:a+eof_num]

                    if byte2==eof_byte2:
                        
                        eof.append(hex(a+eof_num))



        

   
    
    if len(sof) ==0 or len(eof) == 0:
        print('No ',file_type,' files in the given image ')
        return
    
    if os.path.isdir(dir_path):
        print('\nThe directory ',dir_path,' already exists....')

    else:
        try:
            os.mkdir(dir_path)
            print('\nDirectory ',dir_path,' has been created successfully........')
        except:
            print('\nError[Unable to create ',dir_path,' directory]')
            print('\nNote: Works only on linux......Please check your file system, if required change the hardcoded path......Stopping the program...')
            sys.exit()
    b=1    
    for i in sof:
        for j in eof:
            length=int(j,16)-int(i,16)
            if length>0:
                carve_data=data[int(i,16):int(j,16)]
                hash_obj.update(carve_data)
                hash_md5=str(hash_obj.hexdigest())
                carve_filename=str(file_type+'-'+str(b)+file_ext)
                carve_filepath=str(dir_path+carve_filename)
                carve_file=open(carve_filepath,'wb')
                carve_file.write(carve_data)
                carve_file.close()
                b=b+1
                offset=str(i+' and '+j)
                pt=[length,offset,hash_md5]
                file_details[carve_filename]=pt
                hash_str=str(carve_filename+'['+hash_md5+']')
                hash_file=open(hash_path,'a')
                hash_file.write(hash_str)
                hash_file.write('\n')
             





if not len(sys.argv)==2:
    print('Error[Please provide right arguments to proceed]')
    print('\nNote: The arguments should be in the format of <Program_name> <File_name>')
    sys.exit()

else:

    file=sys.argv[1]

    if os.path.exists(file):
        print('\nFile: ',file,' exists...')
        print('\n\nStarting Data carver, Please wait.........')
        
        t=[]
        # Please add the required file formats in the list below
        list_ext=['.pdf','.png','.jpg']
       
      
        for i in list_ext:
            thread=threading.Thread(target=data_carver, args=(file,i))
            print('Thread for ',i,' has started....')
            thread.start()
            t.append(thread)

        for i in t:
            i.join()
            
        output_table()
       

    else:
        print('\nError[File: ',file,' does not exists]')
        print('\nPlease try again with proper file name......')
        sys.exit()

    
