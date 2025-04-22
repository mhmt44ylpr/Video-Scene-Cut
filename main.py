import threading
import customtkinter as ctk
from tkinter import filedialog
import pyfiglet
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import colorama

class My_Darlight_Video_Scenes_Cut(ctk.CTk):

	DURATION_TIME = 8
	BASE_DIR = ''

	def __init__(self):
		super().__init__()

		self.title('Video Scenes Cut')
		self.geometry('600x400')
		self.maxsize(width=600,
					 height=400)
		self.minsize(width=600,
					 height=400)
		self.frame_main = ctk.CTkFrame(master=self,
									   width=590,
									   height=490)
		self.frame_main.place(relx=0.5,
							  rely=0.5,
							  anchor=ctk.CENTER)
		self.MainFrame()
	def MainFrame(self):

		header_label = ctk.CTkLabel(master=self.frame_main,text='Kırpılacak Videonun Kaç Saniyelik Parçalara Ayrılacağını \n Seçip Ondan Sonra Filmi Seçip Videoyu Kırp Butonuna Tıklayabilrisin ')
		header_label.place(relx=0.5,
							 rely=0.28,
							 anchor=ctk.CENTER)

		header_label = ctk.CTkLabel(master=self.frame_main,text='Video Süresi: ')
		header_label.place(relx=0.2,
							 rely=0.4,
							 anchor=ctk.CENTER)
		self.slider = ctk.CTkSlider(self.frame_main,
									from_=8, to=30,
									number_of_steps=22,
									command=self.slider_change)
		self.slider.place(relx=0.5,
							 rely=0.4,
							 anchor=ctk.CENTER)

		self.slider.set(1)

		self.label_value = ctk.CTkLabel(self.frame_main, text="Süre: 8", font=("Arial", 14))
		self.label_value.place(relx=0.8,
							 rely=0.4,
							 anchor=ctk.CENTER)

		self.file_path = ctk.CTkLabel(self.frame_main, text="Dosya Seç: ", font=("Arial", 14))
		self.file_path.place(relx=0.1,
							 rely=0.55,
							 anchor=ctk.CENTER)
		self.path_frame = ctk.CTkFrame(self.frame_main,width=340,fg_color='white',height=20)
		self.path_frame.place(relx=0.48,
							 rely=0.55,
							 anchor=ctk.CENTER)

		self.label_value_value = ctk.CTkLabel(self.path_frame, text="Videoyu Seç", font=("Arial", 10),text_color='black',height=13)
		self.label_value_value.place(relx=0.5,
							 rely=0.5,
							 anchor=ctk.CENTER)

		button_path = ctk.CTkButton(master=self.frame_main,
								   text='Videoyu Seç',
								   width=20,
									command=self.file_change)
		button_path.place(relx=0.9,
						 rely=0.55,
						 anchor=ctk.CENTER)
		button_cut = ctk.CTkButton(master=self.frame_main,
								   text='Videoyu Kırp ',
								   width=100,
								   command=self.Change_to_Scenes)
		button_cut.place(relx=0.5,
						 rely=0.7,
						 anchor=ctk.CENTER)
		self.label_result = ctk.CTkLabel(self.frame_main,text_color='white', text="", font=("Arial", 18))
		self.label_result.place(relx=0.5,
							 rely=0.80,
							 anchor=ctk.CENTER)
	def slider_change(self, value):

		int_value = int(round(value))
		self.label_value.configure(text=f"Süre: {int_value}")
		self.DURATION_TIME = int_value


	def file_change(self):
		dosya_yolu = filedialog.askopenfilename(
			title="Bir dosya seçin",
			filetypes=[("Tüm Dosyalar", "*.*"), ("Metin Dosyaları", "*.txt")]
		)
		if dosya_yolu:
			self.label_value_value.configure(text=f"{dosya_yolu}")
			self.BASE_DIR = dosya_yolu
		else:
			self.label_value_value.configure(text="Dosya seçilmedi.")

	def split_video(self,input_path, output_folder, chunk_duration=8):
		video = VideoFileClip(input_path)
		video_duration = int(video.duration)

		os.makedirs(output_folder, exist_ok=True)

		for start in range(0, video_duration, chunk_duration):
			end = min(start + chunk_duration, video_duration)

			clip = video.subclipped(start, end)

			output_filename = f"{start}-{end}.mp4"
			output_path = os.path.join(output_folder, output_filename)
			self.label_result.configure(text=f"{start}-{end}.mp4 adlı dosya oluşturuldu")
			clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

		self.label_result.configure(text=f"BİTTTİİ")

		ascii_art = pyfiglet.figlet_format("Sevgilim \n Bitti")
		print(colorama.Fore.RED + ascii_art)
	def Change_to_Scenes(self):
		print(self.BASE_DIR)
		print(self.DURATION_TIME)

		def worker():
			try:
				self.split_video(
					self.BASE_DIR,
					output_folder=self.BASE_DIR.split('/')[-1].split('.')[0],
					chunk_duration=self.DURATION_TIME
				)
			except Exception as e:
				self.label_result.configure(text="mp4 uzantılı bir video seçermisin !!!")

		threading.Thread(target=worker).start()
if __name__ == '__main__':

	app = My_Darlight_Video_Scenes_Cut()

	app.mainloop()