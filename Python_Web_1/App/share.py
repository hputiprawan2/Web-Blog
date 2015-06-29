#######################
####### imports #######
#######################
from flask import render_template, request, Blueprint
# import sys, traceback
# from  werkzeug.debug import get_current_traceback

######################
####### config #######
######################
share_blueprint = Blueprint(
	'ShareFiles', __name__,
	template_folder='templates'
)

################################################
####### Set/Get Number of Itmes Per Page #######
################################################

PER_PAGE = 5
def setPER_PAGE(per_page):
	try: 
		if isinstance(per_page, int):
			PER_PAGE=per_page
			return PER_PAGE
	except:
		print 'PER_PAGE is not integer.'

# in case you want to set a new perPage for the entire app
def getPER_PAGE():
	return PER_PAGE


#########################################
####### For Future Implementation #######
#########################################

##########################
####### Error Page #######
##########################
@share_blueprint.route('/error_page')
def error_page():
    return render_template("error_page.html")

################################
####### Show Stack Trace ####### NOT DONE
################################
@share_blueprint.route('/stack_trace')
def stack_trace():
	# trace= get_current_traceback(skip=1, show_hidden_frames=True,
 #            ignore_system_exceptions=False)
	trace = request.args['trace']
	# trace.log()
	# print sys.exc_info()
	# trace = traceback.print_exc().encode('utf-8')
	return render_template("stack_trace.html", trace=trace)