#districts { line-color: #999; line-width: 0.5; polygon-opacity: 0.5; }
@c1: #f3b05d;
@c2: #b3bf7e;
@c3: #8cbcb5;
@c4: #e1582c;
@c5: #5e6f3e;
@c6: #698784;
@c7: #932700;
@c8: #7f985e;
@c9: #204e50;


#districts[SLDUST="ZZZ"] { polygon-opacity: 0; line-opacity: 0; }


#districts[SLDUST="001"] { polygon-fill: @c7; }
#districts[SLDUST="002"] { polygon-fill: @c1; }
#districts[SLDUST="003"] { polygon-fill: @c4; }
#districts[SLDUST="004"] { polygon-fill: @c8; }
#districts[SLDUST="005"] { polygon-fill: @c2; }
#districts[SLDUST="006"] { polygon-fill: @c3; }
#districts[SLDUST="007"] { polygon-fill: @c5; }
#districts[SLDUST="008"] { polygon-fill: @c6; }