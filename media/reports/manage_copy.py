#################Sublime################

wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -

echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list

sudo apt-get update

sudo apt-get install sublime-text


#############Chrome##################

sudo apt install gdebi-core

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo gdebi google-chrome-stable_current_amd64.deb

####################PCharm#########################

sudo snap install pycharm-community --classic
pycharm-community 2017.3.3 from 'jetbrains' installed

https://www.youtube.com/watch?v=OfK01j-L88A


