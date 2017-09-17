# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-09-09 09:59:21
# @Last Modified by:   Lorenzo
# @Last Modified time: 2017-09-17 16:09:39

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

"""
.. module:: sensors_layers

**************
Sensors Layers
**************

Definitions of sensors layers retrieving players data with different sensors dynamics and
characteristics.

    """

class PerfectSensors:
    """
========================
The PerfectSensors class
========================

.. class:: PerfectSensors()

    Create a PerfectSensors instance: a sensors layer capable of retrieving player's position and
    acceleration with no noise or delay.

    """
    def __init__(self):
        pass

    def get_data(self, player):
        """
.. method:: get_data(player)

        Return player position and acceleration with no noise or delay.

        """
        return {'position': player.pos, 'acceleration': player.acc}
