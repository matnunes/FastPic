from smb.SMBConnection import SMBConnection
from guizero import App, PushButton, Text
import threading
import time
import os
import configServer
import logging

# Action you would like to perform
def button_click(button_txt):
    logging.debug('Botao limpar')
    if button_txt == 'Limpar' :
        txtCaso.value = ""
    else :
        txtCaso.value += button_txt

def run_command():    
    logging.debug('START cam')
    os.system('raspistill  -vf -hf --timeout 1 -o /home/pi/FastPicApp/temp_pic.jpg &')
    logging.debug('FINISH cam')
    time.sleep(1)
    system_name = configServer.samba['ip']
    conn = SMBConnection(configServer.samba['user'],configServer.samba['password'],"rasp",configServer.samba['name'])
    logging.debug('START connect SMB')
    try:
        if conn.connect(system_name,139):
            file_obj = open('/home/pi/FastPicApp/temp_pic.jpg', 'rb')
            file_name = time.strftime("%Y%m%d-%H%M%S")

            if caso != "":
                svResponse = conn.listPath(configServer.samba['share'], '/', timeout=60)
                folderExists = False
                for i in range(len(svResponse)):
                    if svResponse[i].filename == caso:
                        folderExists = True
                if not folderExists :
                    conn.createDirectory(configServer.samba['share'],caso)
            logging.debug('WRITE file SMB START')
            conn.storeFile(configServer.samba['share'],caso+'/'+file_name+'.jpg', file_obj)
            logging.debug('WRITE file SMB END')
            conn.close()
        else :
            logging.debug('MSG Erro')
            txtCaso.value = "Erro!"
            time.sleep(4)
    except:
        logging.debug('MSG Erro copiar arquivo')
        print('Erro ao copiar o arquivo')
        txtCaso.value = "Erro!"  	# only displays this after a delay
        time.sleep(2)          		# originally a subprocess is called here; works

    txtCaso.value = "Concluído!"  	# only displays this after a delay
    time.sleep(1)
    txtCaso.value = caso
    camButton.enable()


def cam_click():
    global caso
    caso = txtCaso.value
    txtCaso.value = "Enviando..."
    camButton.disable()
    th = threading.Thread(target=run_command).start()
    th.join()

logging.basicConfig(format='%(asctime)s - %(message)s',level=logging.DEBUG)
caso = ""

app = App("FastPic", layout="grid")

lblCaso = Text(app, text="Digite o caso:", align="left", grid=[3, 0],font="Verdana",size=14,color="black")
txtCaso = Text(app, text="", align="center", grid=[3, 1, 4, 1],font="Verdana",size=16,color="blue")
camButton = PushButton(app, image="camera.png", width=140, height=90, command=cam_click, align="left", grid=[3, 2, 4, 3])

button1 = PushButton(app, text="1", grid=[0,0],width="6",height="2",command=button_click,args=["1"])
button1.tk.config(font=("Verdana",13,"bold"))
button2 = PushButton(app, text="2", grid=[1,0],width="6",height="2",command=button_click,args=["2"])
button2.tk.config(font=("Verdana",13,"bold"))
button3 = PushButton(app, text="3", grid=[2,0],width="6",height="2",command=button_click,args=["3"])
button3.tk.config(font=("Verdana",13,"bold"))
button4 = PushButton(app, text="4", grid=[0,1],width="6",height="2",command=button_click,args=["4"])
button4.tk.config(font=("Verdana",13,"bold"))
button5 = PushButton(app, text="5", grid=[1,1],width="6",height="2",command=button_click,args=["5"])
button5.tk.config(font=("Verdana",13,"bold"))
button6 = PushButton(app, text="6", grid=[2,1],width="6",height="2",command=button_click,args=["6"])
button6.tk.config(font=("Verdana",13,"bold"))
button7 = PushButton(app, text="7", grid=[0,2],width="6",height="2",command=button_click,args=["7"])
button7.tk.config(font=("Verdana",13,"bold"))
button8 = PushButton(app, text="8", grid=[1,2],width="6",height="2",command=button_click,args=["8"])
button8.tk.config(font=("Verdana",13,"bold"))
button9 = PushButton(app, text="9", grid=[2,2],width="6",height="2",command=button_click,args=["9"])
button9.tk.config(font=("Verdana",13,"bold"))
button0 = PushButton(app, text="0", grid=[1,3],width="6",height="2",command=button_click,args=["0"])
button0.tk.config(font=("Verdana",13,"bold"))
buttonP = PushButton(app, text=".", grid=[2,3],width="6",height="2",command=button_click,args=["."])
buttonP.tk.config(font=("Verdana",13,"bold"))
buttonC = PushButton(app, text="Limpar", grid=[0,3],width="6",height="2",command=button_click,args=["Limpar"])
buttonC.tk.config(font=("Verdana",13,"bold"))

app.display()
