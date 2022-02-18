# FastPic

Sistema de captura de foto e upload para um servidor SMB (compartilhamento Windows), permitindo o controle e registro de entrada/saída de objetos. A interface do aplicativo é otimizada para tela 3.5'' com touchscreen do Raspberry Pi. 

O aplicativo permite que o usuário entre um número da pasta (número do caso, por exemplo) para upload das fotos (caso a pasta não exista no compartilhamento ela será criada, se a pasta já existir as fotos serão enviadas para dentro da pasta que existir). Nomes dos arquivos de imagem possuem o timestamp de captura.

FastPic foi desenvolvido em linguagem Python com bibliotecas GuiZero, Threading, SMBConnection e raspistill. As bibliotecas devem ser instaladas *antes* de executar o aplicativo.

## Hardware recomendado

* Raspberry Pi model 3 B ou superior (ex: https://www.robocore.net/placa-raspberry-pi/raspberry-pi-3-model-b-plus)
* Câmera fotográfica v1.3 5MP (ex: https://www.adafruit.com/product/1367)
* Tela 3.5'' com touchscreen (ex: https://www.filipeflop.com/produto/display-compativel-raspberry-pi-touchscreen-5/)
* Sistema de iluminação com LEDs do objeto de interesse 
* Montar o sistema preferencialmente em perfil 2020 ou estrutura de suporte rígida

## Configuração

Edite o arquivo configServer.py com as credenciais e informações do servidor de compartilhamento da sua rede conforme instruções do próprio arquivo.

## Instrução de instalação
1) Clonar o código do Git para o Raspbery Pi (i.e ***git clone https://github.com/matnunes/FastPic.git***)
2) Colocar os arquivos da pasta FastPicApp dentro da pasta de sistema (ex: ***/home/pi***)
3) Copiar o arquivo FastPic para o desktop do Raspberry Pi (ex: ***/home/pi/Desktop***)
4) Executar o aplicativo FastPic na área de trabalho que irá executar o programa, por padrão, no seguinte diretório ***/home/pi/FastPicApp/FastPic.py***
