SRCD = source_fonts
DIST = dists
TMPD = tmp
all: build

build: download
	@[ -d $(TMPD) ] || mkdir -p $(TMPD)
	@[ -d $(DIST) ] || mkdir -p $(DIST)
	python3 build.py
	./fix_AvgCharWidth.sh $(DIST)
	rm -fr $(TMPD)

# download: dl_agave dl_bizud dl_twemoji dl_icons
download: dl_cascadia dl_bizud dl_notoemoji dl_icons

dl_cascadia:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/CascadiaMono-Regular.ttf ] ; then\
	  echo "Download CascadiaMono" ;\
	  wget https://github.com/microsoft/cascadia-code/releases/download/v2111.01/CascadiaCode-2111.01.zip ;\
	  unar CascadiaCode-2111.01.zip ;\
	  cp CascadiaCode-2111.01/ttf/static/CascadiaMono-Regular.ttf \
	     $(SRCD)/CascadiaMono-Regular.ttf ;\
	  cp CascadiaCode-2111.01/ttf/static/CascadiaMono-Bold.ttf \
	     $(SRCD)/CascadiaMono-Bold.ttf ;\
	  rm -f CascadiaCode-2111.01.zip ;\
	  rm -fr CascadiaCode-2111.01 ;\
	fi

dl_bizud:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/BIZUDGothic-Regular.ttf ] ; then\
	  echo "Download Morisawa BIZ UD Gothic" ;\
	  wget https://github.com/googlefonts/morisawa-biz-ud-gothic/releases/download/v1.05/morisawa-biz-ud-gothic-fonts.zip ;\
	  unar morisawa-biz-ud-gothic-fonts.zip ;\
	  cp morisawa-biz-ud-gothic-fonts/fonts/ttf/BIZUDGothic-Regular.ttf \
	    $(SRCD)/BIZUDGothic-Regular.ttf ;\
	  cp morisawa-biz-ud-gothic-fonts/fonts/ttf/BIZUDGothic-Bold.ttf \
	    $(SRCD)/BIZUDGothic-Bold.ttf ;\
	  rm -fr morisawa-biz-ud-gothic-fonts ;\
	  rm -fr morisawa-biz-ud-gothic-fonts.zip ;\
	fi

dl_notoemoji:
	@[ -d $(SRCD) ] ||	mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/NotoEmoji-Regular.ttf ] ; then\
	  echo "Download Noto Emoji Monchrome" ;\
	  wget "https://fonts.google.com/download?family=Noto%20Emoji" -O Emoji.zip;\
	  unar Emoji.zip ;\
	  cp -v Emoji/static/NotoEmoji-Regular.ttf $(SRCD)/ ;\
	  rm -fr Emoji ;\
	  rm -f Emoji.zip ;\
	fi

dl_icons:
	@if [ ! -f $(SRCD)/isfit-plus.ttf ] ; then\
	  wget https://github.com/uwabami/isfit-plus/raw/master/dists/isfit-plus.ttf -O $(SRCD)/isfit-plus.ttf ;\
	fi

clean:
	@rm -f scripts/*.pyc
	@rm -fr scripts/__pycache__

distclean: clean
	rm -fr $(SRCD)/*.ttf
	rm -fr $(DIST)/*.ttf
	rm -fr $(TMPD)
	rm -fr $(DIST)
