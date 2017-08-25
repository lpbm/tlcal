M4 = /usr/bin/m4

BIN_DIR = `pwd`

DESTDIR = /
INSTALL_PREFIX = usr/local/
USERUNITDIR = lib/systemd/system

.PHONY: units
units: units/calendar.service units/calendarevents.service units/tooter.service

units/calendar.service: units/calendar.service.in
	$(M4) -DBIN_DIR=$(BIN_DIR) $< >$@
units/calendarevents.service: units/calendarevents.service.in
	$(M4) -DBIN_DIR=$(BIN_DIR) $< >$@
units/tooter.service: units/tooter.service.in
	$(M4) -DBIN_DIR=$(BIN_DIR) $< >$@



.PHONY: install
install: units
	test -d $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/ || mkdir -p $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/

	cp units/calendar.service $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/
	cp units/calendar.timer $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/
	cp units/calendarevents.service $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/
	cp units/calendarevents.timer $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/
	cp units/tooter.service $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/
	cp units/tooter.timer $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/

.PHONY: uninstall
uninstall:
	$(RM) $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/calendar.service
	$(RM) $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/calendar.timer
	$(RM) $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/calendarevents.service
	$(RM) $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/calendarevents.timer
	$(RM) $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/tooter.service
	$(RM) $(DESTDIR)$(INSTALL_PREFIX)$(USERUNITDIR)/tooter.timer

.PHONY: clean
clean:
	$(RM) units/calendar.service
	$(RM) units/calendarevents.service
	$(RM) units/tooter.service
