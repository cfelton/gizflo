# Copyright (c) 2014 Christopher Felton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from __future__ import print_function

from myhdl import enum

#from .._report_parser import ReportParser

def get_fmax(fn, info):
    log = open(fn, 'r')
    fmax = []
    States = enum('search', 'fmax')
    state = States.search
    glncnt,lncnt = 0,0

    for ln in log:
        if state == States.search:
            if glncnt > 100 and 'Fmax Summary' in ln:
                lncnt = 1
                state = States.fmax

        elif state == States.fmax:
            if lncnt == 5:
                fstr = ln.split(';')
                if len(fstr) < 2:
                    state = States.search
                    continue
                fstr = fstr[1].split()
                fstr = fstr[0].strip()
                fmax.append(fstr)

            if lncnt >= 6:
                state = States.search

        lncnt += 1
        glncnt += 1

    if len(fmax) > 0:
        info['fmax'] = min(map(float, fmax))
    else:
        info['fmax'] = -1
    
    return info
    


def get_utilization(fn=None):
    """ parse teh device resource utilization from the logs

    @todo : the following is fairly ugly and not the most 
       reliable.  There are xml files create (xrp) that would
       be a better source for the utilization - once the xlm
       package is understood these reports can be used instead
       of the log.    
    """

    log = open(fn, 'r')
    info = {}
    info['syn'] = {}
    fmax = []
    States = enum('search', 'le_util', 'io_util', 'ip_util')
    state = States.search
    glncnt,lncnt = 0,0

    #  5 "Total logic elements"
    # 20 "Total registers"
    # 34 "Embedded Multiplier"
    # these change in differen revisions
    usage_lines = [5, 20, 34]

    for ln in log:
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if state == States.search:
            if glncnt == 2:
                version = ln.split('Version ')[1]
                splitlist = version.split(' ')
                version = splitlist[0]

            if glncnt > 60 and glncnt < 80 and 'Family' in ln:
                if 'Cyclone V' in ln:
                    usage_lines = [5, 34, 79]
            if glncnt > 64 and 'Fitter Resource Usage Summary' in ln:
                state = States.le_util
                lncnt = 1

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif state == States.le_util:
            ln = ln.strip()
            if lncnt in usage_lines:
                sp1 = ln.split(';')
                if len(sp1) != 4 and len(sp1) != 5:
                    state = States.search
                    continue
                    
                sp2 = sp1[2]
                sp2 = sp2.replace('<', '')
                sp2 = sp2.replace('(', '')
                sp2 = sp2.replace(')', '')
                sp2 = sp2.split()
                if len(sp2) != 5 and len(sp2) != 3:
                    state = States.search
                    continue  # jump to the next line

                usage = ln.split(';')
                if len(usage) == 4:    
                    pd,nm,outof,ju = usage
                elif len(usage) == 5:
                    pd1,nm,outof,per,pd2 = usage
                outof = outof.replace('<', '')
                outof = outof.replace('(', '')
                outof = outof.replace(')', '')
                outof = outof.split()
                if len(outof) == 5:
                    x,slash,y,p,ps = outof
                elif len(outof) == 3:
                    x,slash,y = outof
                    per = per.strip().split(' ')
                    p = per[-2]
                    ps = per[-1]
                x = x.replace(',', '')
                y = y.replace(',', '')
                
            if lncnt == usage_lines[0]:
                info['syn']['lut'] = tuple(map(int, (x,y,p,)))
            elif lncnt == usage_lines[1]:
                info['syn']['reg'] = tuple(map(int, (x,y,p,)))
            elif lncnt == usage_lines[2]:
                info['syn']['dsp'] = tuple(map(int, (x,y,p,)))
            # @todo: memory bits
            elif lncnt >= 100:
                state = States.search

        # keep track which line, reset for sections
        lncnt += 1
        glncnt += 1

        # end of parsing state-machine
        
    
    return info
