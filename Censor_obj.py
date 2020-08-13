from pydub import AudioSegment
from shutil import copyfile
import os
import logging


class Rbt(object):

        def __init__(self, source_path, file_name):

                self.rbt_name = file_name
                self.rbt_id = 0
                self.rbt_censor_period = []
                self.rbt_file_path = source_path + '/' + file_name

        def cut_places(self, rbt_name):

                floor_list = []
                counter = 0
                for char in str(rbt_name):
                       if char == '_':
                                floor_list.append(counter)

                       counter = counter + 1


                range_list = []
                for indx, value in enumerate(floor_list):
                        if len(floor_list[indx:indx+2]) > 1:
                                temp_string = rbt_name[value+1: floor_list[indx+1]]
                                range_list.append(rbt_name[value+1: floor_list[indx+1]])


                self.rbt_censor_period = range_list

        def cut_id(self, rbt_name):

                status = True
                counter = 0
                i = 0
                while status == True:
                        i += 1
                        if rbt_name[i] == '_':
                                self.rbt_id = rbt_name[:i]
                                status = False



def censor(rbt_obj, source_path):

        original_track = AudioSegment.from_file(rbt_obj.rbt_file_path, format="mp3")
        #print(rbt_obj.rbt_censor_period)

        for period in rbt_obj.rbt_censor_period:
                #
                char_indx = period.find('-')
                A = int(period[0:char_indx])
                B = int(period[char_indx+1:])
                #
                track_part_A = original_track[0:(A*1000)]
                track_part_B = original_track[(B*1000):]
                track_to_reverse = original_track[(A*1000):(B*1000)]
                track_to_reverse = track_to_reverse.reverse()

                original_track = track_part_A + track_to_reverse + track_part_B

        #tworzę ocenzurowany plik temp.mp3
        original_track.export(source_path+'/_Gotowe/_temp'+rbt_obj.rbt_id+'.mp3')
        #ffmpeg konwertuje plik temp.mp3 pod właściwe parametry do serwisu Orange
        os.system('ffmpeg -i '+'"'+source_path+'/_Gotowe/_temp'+rbt_obj.rbt_id+'.mp3'+'"'+' -ar 44100 -ac 1 -ab 64k -id3v2_version 0 '+'"'+source_path+'/_Gotowe/'+rbt_obj.rbt_id+'.mp3'+'"')
        os.system('ffmpeg -i '+'"'+source_path+'/_Gotowe/_temp'+rbt_obj.rbt_id+'.mp3'+'"'+' -c:a pcm_alaw -ar 8000 -ac 1 -bitexact '+'"'+source_path+'/_Gotowe/'+rbt_obj.rbt_id+'.wav'+'"')
        #usuwam temp.mp3
        os.remove(source_path+'/_Gotowe/_temp'+rbt_obj.rbt_id+'.mp3')
        

def main():
        #path to the script AND audio files(.mp3)
        main_folder_path = os.getcwd()
        file_list = os.listdir(main_folder_path)

        if not os.path.exists(main_folder_path+'/_Gotowe'):
                os.makedirs(main_folder_path+'/_Gotowe')

        mp3_to_convert_list = []
        #pętla po każdym pliku w folderze
        for file_name in file_list:
                #wyłapuje same mp3
                if '.mp3' in file_name:
                        #wylapuje audio z okresem do ocenzurowania zapisanym miedzy podlogami "_03-07_"
                        if file_name.count('_') > 1:
                                # TWORZĘ OBIEKT o nazwie pliku "242823_00-01_03-04_06-10_59-60_.mp3"
                                file_name = Rbt(main_folder_path, file_name)
                                # tworzę za pomocą metody classy Rbt listę okresów do ocenzurowania 00-01 + 03-04 + 06-10 + 59-60
                                file_name.cut_places(file_name.rbt_name)
                                # przypisuję dla obietku id ringbacktonea: 242823
                                file_name.cut_id(file_name.rbt_name)
                                #zbieram wszystkie obiekty do listy
                                mp3_to_convert_list.append(file_name)


        for rbt_obj in mp3_to_convert_list:
                censor(rbt_obj, main_folder_path)
                #print(.rbt_name)

        #sprawdzenie
        for i in mp3_to_convert_list:
                #print(i.rbt_name)
                print(i.rbt_id)
                print(i.rbt_censor_period)
                print(i.rbt_file_path)
                print('\n')


main()
