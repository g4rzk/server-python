# import module
import os
import time
import sqlite3
import datetime
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.measure import Measurement
from rich.table import Table

os.system("clear")
garzk_db = sqlite3.connect("database/garzk.db")

c = garzk_db.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS garzk(
license integer not null primary key,
pengguna text,
bergabung interger,
kadaluarsa interger);""")

date_object = datetime.date.today()

class Server:
	
	def __init__(self):
		self.no = 0
		self.user = "admin"
		self.pw = "admin"
		
	#method login untuk akses database
	def loginServer(self):
		user = input(" [?] Masukan User : ")
		if user == self.user:
			pw = input(" [?] Masukan Pass : ")
			self.backtoMenu()
		else:
			exit("\n [!] Gagal Login...!")
	
	# method masukan data ke database
	def insertData(self, license, pengguna, bergabung, kadaluarsa):
		c.execute(f"INSERT INTO garzk VALUES( \
			{license}, \
			'{pengguna}', \
			'{bergabung}', \
			'{kadaluarsa}' \
		)") 
		garzk_db.commit()
	
	# update data di database
	def updateData(self, license, pengguna, bergabung, kadaluarsa):
		c.execute(f"UPDATE garzk SET \
			pengguna = '{pengguna}', \
			bergabung = '{bergabung}', \
			kadaluarsa = '{kadaluarsa}' \
			WHERE license = {license} \
		")
		garzk_db.commit()
	
	# delete data di database
	def deleteData(self, license):
		c.execute(f"DELETE FROM garzk \
			WHERE license = {license} \
		")
		garzk_db.commit()
		
	# method melihat semua data di database
	def showData(sef):
		table = Table("License", "Pengguna", "Bergabung", "Kadaluarsa")
		c.execute("SELECT * FROM garzk ORDER BY license ASC")
		for i in c.fetchall():
			license = i[0]
			pengguna = i[1]
			bergabung = i[2]
			kadaluarsa = i[3]
			
			# masukan semua data di table rich
			table.add_row(f"{license}", f"{pengguna}", f"{bergabung}", f"{kadaluarsa}")
		console = Console()
		console.print(table, justify="center")
	
	# method back to menu
	def backtoMenu(self):
		time.sleep(2)
		os.system("clear")
		self.showData()
		self.menuServer()
	
	# method menu server
	def menuServer(self):
		print(Panel(f"[1]. Masukan Data\n[2]. Ubah Data\n[3]. Hapus Data\n[4]. Keluar", title="MENU SERVER"))
		ask = input(" [?] Chooice : ")
		if ask in (""):
			self.backtoMenu()
		
		# masukan data ke database
		elif ask in ("1"):
			os.system("clear")
			print(Panel(f"Contoh Format Data\nLicense    : 1020304050607080\nPengguna   : Angga\nBergabung  : {date_object}\nKadaluarsa : {date_object}", title="MASUKAN DATA"))
			license = int(input(" [?] License    : "))
			pengguna = input(" [?] Pengguna   : ")
			bergabung = input(" [?] Bergabung  : ")
			kadaluarsa = input(" [?] Kadaluarsa : ")
			try:
				self.insertData(license, pengguna.title(), bergabung.title(), kadaluarsa.title())
				print(Panel(f"Berhasil Memasukan Data {pengguna}", title="INFORMASI"))
				self.backtoMenu()
			except:
				print(Panel(f"Gagal Memasukan Data {pengguna}", title="INFORMASI"))
				self.backtoMenu()
		
		# ubah data di database
		elif ask in ("2"):
			os.system("clear")
			self.showData()
			license = int(input(" [?] Masukan License    : "))
			c.execute(f"SELECT COUNT(*) FROM garzk WHERE license LIKE '%{license}%'")
			result = c.fetchone()
			if result[0] == 0:
				print(Panel(f"{license} tidak ada di database", title="INFORMASI"))
				self.backtoMenu()
			else:
				c.execute(f"SELECT * FROM garzk WHERE license LIKE '%{license}%'")
				for i in c.fetchall():
					license = i[0]
					pengguna = i[1]
					bergabung = i[2]
					kadaluarsa = i[3]
					os.system("clear")
					print(Panel(f"License    : {license}\nPengguna   : {pengguna}\nBergabung  : {bergabung}\nKadaluarsa : {kadaluarsa}", title="UBAH DATA"))
					pengguna = input(" [?] Pengguna   : ")
					bergabung = input(" [?] Bergabung  : ")
					kadaluarsa = input(" [?] Kadaluarsa : ")
					try:
						self.updateData(license, pengguna.title(), bergabung.title(), kadaluarsa.title())
						print(Panel(f"Berhasil Update Data {pengguna}", title="INFORMASI"))
						self.backtoMenu()
					except:
						print(Panel(f"Gagal Update Data {pengguna}", title="INFORMASI"))
						self.backtoMenu()
		
		# hapus data di database
		elif ask in ("3"):
			os.system("clear")
			self.showData()
			license = int(input(" [?] Masukan License    : "))
			c.execute(f"SELECT COUNT(*) FROM garzk WHERE license LIKE '%{license}%'")
			result = c.fetchone()
			if result[0] == 0:
				print(Panel(f"{license} tidak ada di database", title="INFORMASI"))
				self.backtoMenu()
			else:
				c.execute(f"SELECT * FROM garzk WHERE license LIKE '%{license}%'")
				for i in c.fetchall():
					license = i[0]
					pengguna = i[1]
					bergabung = i[2]
					kadaluarsa = i[3]
					os.system("clear")
					print(Panel(f"License    : {license}\nPengguna   : {pengguna}\nBergabung  : {bergabung}\nKadaluarsa : {kadaluarsa}", title="HAPUS DATA"))
					askAgain = input(" [?] Apakah anda yakin ingin menghapus [Y/t]: ")
					if askAgain in ("Y", "y"):
						self.deleteData(license)
						print(Panel(f"Berhasil Hapus Data {pengguna}", title="INFORMASI"))
						self.backtoMenu()
					else:
						self.backtoMenu()
		else:
			self.backtoMenu()

run = Server()
#run.loginServer()
run.showData()
run.menuServer()

# menutup cursor
c.close()
# menutup koneksi database
garzk_db.close()
