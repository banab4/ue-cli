import unreal

filter_class = "{filter_class}"

world = unreal.EditorLevelLibrary.get_editor_world()

if filter_class and filter_class != "*":
    cls = getattr(unreal, filter_class, None)
    if not cls:
        unreal.log_error("Unknown class: " + filter_class)
    else:
        actors = unreal.GameplayStatics.get_all_actors_of_class(world, cls)
else:
    actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)

for actor in actors:
    label = actor.get_actor_label()
    name = actor.get_name()
    cls_name = actor.get_class().get_name()
    loc = actor.get_actor_location()
    unreal.log("ACTOR: " + label + " | " + name + " | " + cls_name + " | " + str(loc))

unreal.log("Total: " + str(len(actors)) + " actors")
