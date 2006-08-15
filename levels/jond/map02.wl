#"pickups.h"
#"pipes.wl"

main {

  slimeinit
  floor("SLIME16")

  -- curve out-of-sight
  turnaround
  move(-512)
  twice( slimecurve(0,0) )
  
  -- fade into colour
  set("itr",0)
  for(1,15,
    slimecorridor(16,0,mul(get("itr"),8))
    set("itr",add(1,get("itr")))
  )
  -- no entry!
  slimebars(0,128,120,0)

  -- level starts properly
  pushpop( 
    movestep(384,384) rotright
    slimechoke(0,120)
  )
  slimecurve_r(0,120)
  move(32)

  pushpop( move(640) slimechoke(0,120) )
  slimecorridor(64,0,120)
  slimeopening(512,0,120)
  slimecorridor(64,0,120)
  !entrancecorridor

  movestep(-512,256)
  box(32,128,136,384,128)
  pushpop( movestep(64,64) rotleft thing )
  movestep(0,-384)
  box(32,128,136,384,128)

  ^entrancecorridor
  move(32) -- avoid choke
  slimeswitch(128,0,128,120,1)
  slimebars(0,128,120,1)
  slimecurve(0,120)
  slimecorridor(256,0,120)
  slimesecret(256,0,120, doublebarreled thing)
  slimecorridor(128,0,120)

  pushpop(movestep(384,384) rotright slimechoke(0,120) )
  slimesplit(0,120,

    -- left branch
    slimecorridor(1024,0,120) 
   ,
     
    -- inaccessible bit
--    slimechoke(0,120)
    move(32)
    slimebars(0,128,120,0)
    -- fade into colour
    set("itr",0)
    for(1,15,
      slimecorridor(16,0,sub(mul(8,15),mul(get("itr"),8)))
      set("itr",add(1,get("itr")))  
    )
    slimecurve_r(0,0)
    slimecurve_r(0,0)
  )
}

oldmain {

  slimeinit
  floor("SLIME16")

  set("frad",1)
  pushpop( movestep(64,64) thing )

  for(1,3,
    slimecorridor(256,0,120)
    scurve(0,128,120)
    slimeswitch(256,0,128,120,get("frad"))
    slimebars(0,128,120,get("frad"))
    set("frad",add(1,get("frad")))
  )
  /*
  set("frad",-8)
  for(1,8,
    slimecorridor(16,get("frad"),120)
    set("frad",sub(get("frad"),16))
  )*/
  

  slimesecret(256,get("frad"),120,
    doublebarreled thing
  )

  
  
  
}
