from pydub import AudioSegment
from shutil import copyfile
import os
import logging

def censor(range_list, file_path):

        if file_path.endswith('.mp3'):
                original_track = AudioSegment.from_file(file_path, format="mp3")
#potrafi urwac
        if file_path.endswith('.wav'):
                original_track = AudioSegment.from_file(file_path, format="wav")

         
        for pair in range_list:
                char_indx = pair.find('-')
                A = int(pair[0:char_indx])
                B = int(pair[char_indx+1:])

                track_part_A = original_track[0:(A*1000)]
                track_part_B = original_track[(B*1000):]
                track_to_reverse = original_track[(A*1000):(B*1000)]
                track_to_reverse = track_to_reverse.reverse()

                original_track = track_part_A + track_to_reverse + track_part_B





        original_track.export(os.getcwd()+'/asd'+file_path[37:], format='mp3')
        return 0
	
def cut_places(file_name):

        print(file_name)
        floor_list = []
        counter = 0
        for char in file_name:
                if char == '_':
                        floor_list.append(counter)

                counter = counter + 1

        range_list = []
        for indx, value in enumerate(floor_list):
                if len(floor_list[indx:indx+2]) > 1:
                        temp_string = file_name[value+1: floor_list[indx+1]]
                        range_list.append(file_name[value+1: floor_list[indx+1]])

                
        #print(range_list)
        return range_list

def main():
        #przypisuje aktualna sciezke z miejsca skryptu
        source_path = os.getcwd()
        print(source_path)

        #tworzę listę plikow w folderze gdzie jest skrypt
        file_list = os.listdir(source_path)
        print(file_list)

        #pętla po każdym pliku w folderze
        for file_name in file_list:
                #wyłapuje mp3 i wavcut_places
                if '.mp3' in file_name or '.wav' in file_name:
                        #wyłapuje pliki z przekleństawamit
                        if file_name.count('_') > 1:
                                #scieżka do pliku
                                file_path = source_path + '/' + file_name
                                #odpalam funkcje do wylapywania zakresów z przekleństwem
                                range_list= []
                                range_list = cut_places(file_name)
                                #print(range_list)

                                censor(range_list, file_path)

                                


                                
                                
        return 0


main()
def qwe():

        string= 'asd'
        print(string[5:])
        return 0

#qwe()
