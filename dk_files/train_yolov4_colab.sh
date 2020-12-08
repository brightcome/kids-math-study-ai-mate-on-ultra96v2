# Copyright 2020 Xilinx Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

cd /content/darknet
./darknet detector train -map \
/content/Vitis-In-Depth-Tutorial/Machine_Learning/Design_Tutorials/07-yolov4-tutorial/dk_files/obj.data \
/content/Vitis-In-Depth-Tutorial/Machine_Learning/Design_Tutorials/07-yolov4-tutorial/dk_model/yolov4-leaky_poker.cfg \
/content/Vitis-In-Depth-Tutorial/Machine_Learning/Design_Tutorials/07-yolov4-tutorial/dk_model/yolov4-leaky_best.weights \
-dont_show \
-clear
