include ../build.mk

TRUSTSDIRS=newsearch

.PHONY: all dirs $(TRUSTSDIRS) clean distclean

all: trusts.so trusts_commands.so trusts_policy.so trusts_migration.so trusts_db.so trusts_management.so trusts_master.so trusts_slave.so trusts_api.so dirs

trusts.so: trusts.o data.o formats.o events.o

trusts_db.so: trusts_db.o

trusts_commands.so: trusts_commands.o

trusts_policy.so: trusts_policy.o

trusts_migration.so: trusts_migration.o db-migration.o migration.o

trusts_management.so: trusts_management.o

trusts_master.so: trusts_master.o

trusts_slave.so: trusts_slave.o db-slave.o

trusts_api.so: trusts_api.o

dirs: $(TRUSTSDIRS)
	ln -sf */*.so .

$(TRUSTSDIRS):
	cd $@ && $(MAKE) $(MFLAGS) all

clean:
	rm -f */*.o */*.so *.o *.so
	rm -rf */.deps .deps

distclean:

