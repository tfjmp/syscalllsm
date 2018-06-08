import sqlite3
import sys

def getID(name, cursor):
	'''
	This function gets the ID of the give function `name` in system call database.

	@param name The name of the function
	@param cursor The cursor that traverses through the SQLite database
	@return None or the ID (as a one-element list) of the system call in the database
	'''
	cursor.execute('SELECT f.Id FROM functions AS f WHERE Name = ?', (name,))
	ids = []
	for fid in cursor.fetchall():
		ids.append(fid[0])
	if len(ids) != 1:
		print "Error in function name: " + name
		return None
	else:
		return ids

def replaceName(orig_name):
	'''
	For a list of system calls, the entry point should be replaced with that of its equivalent system call due to kernel implementation.
	Therefore, when we get the ID, we want to get the ID of the replaced function name, not the original one.

	@param orig_name The original name of the function
	@return The replaced name of the function (i.e., the name of the equivalent function)
	'''
	if orig_name == "SyS_dup2":
		return "SyS_dup3"
	elif orig_name == "SyS_mknod":
		return "SyS_mknodat"
	elif orig_name == "SyS_mkdir":
		return "SyS_mkdirat"
	elif orig_name == "SyS_symlink":
		return "SyS_symlinkat"
	elif orig_name == "SyS_link":
		return "SyS_linkat"
	elif orig_name == "SyS_renameat":
		return "SyS_renameat2"
	elif orig_name == "SyS_rename":
		return "SyS_renameat2"
	elif orig_name == "SyS_creat":
		return "SyS_open"
	elif orig_name == "SyS_access":
		return "SyS_faccessat"
	elif orig_name == "SyS_chmod":
		return "SyS_fchmodat"
	elif orig_name == "SyS_chown":
		return "SyS_fchownat"
	elif orig_name == "SyS_lchown":
		return "SyS_fchownat"
	elif orig_name == "SyS_lchown16":
		return "SyS_fchownat"
	elif orig_name == "SyS_chown16":
		return "SyS_fchownat"
	elif orig_name == "SyS_fchown16":
		return "SyS_fchown"
	elif orig_name == "SyS_pipe":
		return "SyS_pipe2"
	elif orig_name == "SyS_utimes":
		return "SyS_futimesat"
	elif orig_name == "sys_getpgrp":
		return "SyS_getpgid"
	elif orig_name == "SyS_mmap":
		return "SyS_mmap_pgoff"
	elif orig_name == "SyS_sigpending":
		return "SyS_rt_sigpending"
	elif orig_name == "SyS_waitpid":
		return "SyS_wait4"
	elif orig_name == "SyS_oldumount":
		return "SyS_umount"
	elif orig_name == "SyS_fadvise64":
		return "SyS_fadvise64_64"
	elif orig_name == "SyS_readlink":
		return "SyS_readlinkat"
	elif orig_name == "SyS_setregid16":
		return "SyS_setregid"
	elif orig_name == "SyS_setgid16":
		return "SyS_setgid"
	elif orig_name == "SyS_setreuid16":
		return "SyS_setreuid"
	elif orig_name == "SyS_setuid16":
		return "SyS_setuid"
	elif orig_name == "SyS_setresuid16":
		return "SyS_setresuid"
	elif orig_name == "SyS_setresgid16":
		return "SyS_setresgid"
	elif orig_name == "SyS_setfsuid16":
		return "SyS_setfsuid"
	elif orig_name == "SyS_setfsgid16":
		return "SyS_setfsgid"
	elif orig_name == "SyS_epoll_create":
		return "SyS_epoll_create1"
	elif orig_name == "sys_inotify_init":
		return "SyS_inotify_init1"
	elif orig_name == "SyS_sync_file_range2":
		return "SyS_sync_file_range"
	elif orig_name == "SyS_signalfd":
		return "SyS_signalfd4"
	elif orig_name == "SyS_eventfd":
		return "SyS_eventfd2"
	elif orig_name == "C_SYSC_x86_truncate64":
		return "SyS_truncate"
	elif orig_name == "C_SYSC_x86_ftruncate64":
		return "SyS_ftruncate"
	elif orig_name == "SyS_accept":
		return "SyS_accept4"
	elif orig_name == "SyS_send":
		return "SyS_sendto"
	elif orig_name == "SyS_recv":
		return "SyS_recvfrom"
	else:
		return orig_name

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print '''
			usage: python syscall.py <database_file_path> <syscall_list_file_path> <output_file_path>
			'''
		exit(1)
	output = open(sys.argv[3], "w+")
	conn = sqlite3.connect(sys.argv[1])
	c = conn.cursor()
	with open(sys.argv[2], 'r') as f:
		for line in f:
			funcname = line.strip()
			print "FuncName: " + funcname + "\n"
			name = replaceName(funcname)
			print "ReplaceName: " + name + "\n"
			id = str(getID(name, c)[0])
			print "ID: " + id + "\n"
			outline = funcname + '\t' + id + '\n'
			output.write(outline)
	f.close()
	output.close()
	conn.close()
