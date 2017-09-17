# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-08-21 13:40:21
# @Last Modified by:   Lorenzo
# @Last Modified time: 2017-09-17 16:09:51

# Copyright 2017 Lorenzo Rizzello
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

_conv_factors = { 
    # 80 meteres -> 800 pix
    'meters_pix' : 800/80
}

for desc, factor in _conv_factors.items():
    units = desc.split('_')
    globals()['_to_'.join(units)] = lambda unit_1: unit_1 * factor
    globals()['_to_'.join(reversed(units))] = lambda unit_2: unit_2 / factor
