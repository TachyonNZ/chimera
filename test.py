import yaml, random, argparse
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open('test.yaml', 'r') as file:
	raw_dict = yaml.load(file, Loader=Loader)

already_changed = []
parts = []
animals = []
activities = []
furLocations = []
robotstring = ""

nontf = ["natural oddity","closet monster","freak of nature","synthetic being","cybernetically enhanced being","organic robot","alien","eldritch minor god","incarnated spirit","child's imaginary friend"]
synth = ["synthetic being","cybernetically enhanced being","organic robot"]
magic = ["magic experiment","eldritch minor god","incarnated spirit","wizard's minion","reincarnated being","victim of a mischevious spirit",]

''' Given a dictionary (choices) and zero or more keys to look under (cat),
    returns randomly selected string from inside the dictionary. '''
def choose(choices,*cat):
    if cat:
        ''' If at least one argument has been passed in addition to the
            dictionary, we know that this isn't being called recursively.
            So we can pull out the parts of the dictionary that we care
            about and then grab a random choice from them. '''
        processed = []
        for s in cat:
            processed += choices.get(s)
        choice = random.choice(processed)
    else:
        ''' If not category arguments have been passed, we assume that
            the dict is already in a processed form. So it's safe to just
            randomly choose an item from it. '''
        processed = list(choices.values())
        if len(processed) is not 1:
            raise Exception("Poorly formatted YAML, some results are impossible.")
        choice = random.choice(processed[0])

    ''' If the choice we've found is a dictionary or list, start
        recursion to find a final value. If it's just a string we
        assume that everything is fine and pass it back out. '''
    if isinstance(choice, (dict, list)):
        return choose(choice)
    elif isinstance(choice, (str)):
        return choice
    else:
        raise Exception("Found an invalid object in dictionary structure!")

def generateRobotParts():
    robocations = []
    robotype = []
    robs = choose(raw_dict,"fur_locations")
    for i in range(random.randrange(2,5)):
        while robs in robocations:
            robs = choose(raw_dict,"fur_locations")
        robocations.append(robs)

    for i in range(len(robocations)):
        robotype.append(choose(raw_dict,"robot_descriptors"))
    if "entire body" in furLocations:
        robocations = ["entire body"]
    if "none" in robocations:
        robocations.remove("none")
    return robocations,robotype

familyname = ""

def nameGen(intelligence,gender,family):
    global familyname
    if intelligence in ["beast","hybrid"]:
        final = "{}'{}".format(
            choose(raw_dict,intelligence+"_names_"+gender),
            choose(raw_dict,intelligence+"_names_suffix")
            ).lower().title()
    elif intelligence == "human":
        if family == "none":
            familyname = choose(raw_dict,"human_last_names")
        final = "{} {}".format(
            choose(raw_dict,"human_names_"+gender),
            familyname
            ).lower().title()
    elif intelligence == "supernatural":
        partOne   = choose(raw_dict,"super_first_names")
        partTwo   = choose(raw_dict,"super_mid_names")
        partThree = choose(raw_dict,"super_seperators")
        partFour  = choose(raw_dict,"super_last_prefix")
        partFive  = choose(raw_dict,"super_last_suffix")
        if family != "none":
            partFour = family
            partFive = ""
        else:
            familyname = partFour+partFive

        final = partOne+partThree+partTwo+" "+partFour+partFive
        final = final.lower()
        final = final.title()
    else:
        raise Exception("Invalid intelligence descriptor: " + intelligence)

    return final

def generateFamily(origin,intelligence,transmission,gender,familyname):
    family = ""
    mate = ""
    mateOrigin = ""
    family = ""
    children = ""
    if intelligence == "beast" and transmission != "none" or origin in nontf:
        if random.randint(1,1) == 1 and "search for a mate" not in activities:
            mate = nameGen(intelligence,gender,familyname)
            mateOrigin = transmission
            #######

            childrenNo = random.randint(0,4)
            children = []
            for i in range(childrenNo):
                children.append(nameGen(intelligence,choose(raw_dict,"sex"),familyname))
        else:
            family = "none"
    if intelligence == "hybrid" and transmission != "none" or origin in nontf:
        if random.randint(1,1) == 1 and "search for a mate" not in activities:
            mate = nameGen(intelligence,gender,familyname)
            mateOrigin = transmission
            #######

            childrenNo = random.randint(0,3)
            children = []
            for i in range(childrenNo):
                children.append(nameGen(intelligence,choose(raw_dict,"sex"),familyname))
        else:
            family = "none"

    if intelligence == "human" and transmission != "none" or origin in nontf:
        if random.randint(1,1) == 1 and "search for someone crazy enough to like you" not in activities:
            mate = nameGen(intelligence,gender,familyname)
            mateOrigin = transmission
            #######

            childrenNo = random.randint(0,2)
            children = []
            for i in range(childrenNo):
                children.append(nameGen(intelligence,choose(raw_dict,"sex"),familyname))
        else:
            family = "none"
    if intelligence == "supernatural" and transmission != "none" or origin in nontf:
        if random.randint(1,1) == 1:
            mate = nameGen(intelligence,gender,familyname)
            mateOrigin = transmission
            #######

            childrenNo = random.randint(0,1)
            children = []
            for i in range(childrenNo):
                children.append(nameGen(intelligence,choose(raw_dict,"sex"),familyname))
        else:
            family = "none"
    else:
        family = "none"

    if mateOrigin == "none" or mateOrigin == "":
        mateOrigin = "indeterminate"

    return mate, mateOrigin, children



def printOut(quantity):

    intelligence = choose(raw_dict,"anthroscale")
    disposition = ""
    for i in range(quantity):
        part = choose(raw_dict,"body_parts")
        while part in parts:
            part = choose(raw_dict,"body_parts")
        parts.append(part)

    for i in range(quantity+1):
        animal = choose(raw_dict,"animals")
        while animal in animals:
            animal = choose(raw_dict,"animals")
        animals.append(animal)

    if intelligence != "beast":
        for i in range(1):
            animal = choose(raw_dict,"animals")
            animals.append(animal)

    for i in range(3):


        if intelligence == "beast":
            act = choose(raw_dict,"beast_activities")
            while act in activities:
                act = choose(raw_dict,"beast_activities")
            activities.append(act)
            averageAge = 8
            disposition = choose(raw_dict,"animal_dispositions")

        elif intelligence == "hybrid":
            act = choose(raw_dict,"hybrid_activities")
            while act in activities:
                act = choose(raw_dict,"hybrid_activities")
            activities.append(act)
            averageAge = 15
            disposition = choose(raw_dict,"animal_dispositions")

        elif intelligence == "human":
            if random.randint(0,1) == 0:
                act = choose(raw_dict,"human_activities_withdrawn")
                while act in activities:
                    act = choose(raw_dict,"human_activities_withdrawn")
                activities.append(act)
                averageAge = 30
                disposition = "withdrawn"
            else:
                act = choose(raw_dict,"human_activities_uncaring")
                while act in activities:
                    act = choose(raw_dict,"human_activities_uncaring")
                activities.append(act)
                averageAge = 30
                disposition = "friendly"



        elif intelligence == "supernatural":
            act = choose(raw_dict,"supernatural_activities")
            while act in activities:
                act = choose(raw_dict,"supernatural_activities")
            activities.append(act)
            averageAge = 120
            disposition = "changing"

    furLocations = []
    furs = choose(raw_dict,"fur_locations")
    for i in range(random.randrange(1,5)):
        while furs in furLocations:
            furs = choose(raw_dict,"fur_locations")
        furLocations.append(furs)
    if "none" in furLocations:
        furLocations = ["none"]
    elif "entire body" in furLocations:
        furLocations = ["entire body"]

    age = averageAge + random.randrange(-int(round((averageAge/10)*5)),int(round((averageAge/10)*5)))

    lifeStage = ""
    if intelligence == "beast":
        if age < 3:
            lifeStage = "young"
        elif age < 5:
            lifeStage = "teenager"
        elif age < 8:
            lifeStage = "adult"
        elif age <= 13:
            lifeStage = "middle-aged"
        elif age > 13:
            lifeStage = "elderly"
    elif intelligence == "hybrid":
        if age < 6:
            lifeStage = "young"
        elif age < 10:
            lifeStage = "teenager"
        elif age < 16:
            lifeStage = "adult"
        elif age <= 20:
            lifeStage = "middle-aged"
        elif age > 20:
            lifeStage = "elderly"
    elif intelligence == "human":
        if age < 13:
            lifeStage = "young"
        elif age < 20:
            lifeStage = "teenager"
        elif age < 40:
            lifeStage = "adult"
        elif age <= 50:
            lifeStage = "middle-aged"
        elif age > 50:
            lifeStage = "elderly"
    elif intelligence == "supernatural":
        if age < 30:
            lifeStage = "young"
        elif age < 60:
            lifeStage = "teenaged"
        elif age < 160:
            lifeStage = "adult"
        elif age <= 180:
            lifeStage = "middle-aged"
        elif age > 180:
            lifeStage = "elderly"
    else:
        lifeStage = "bobRoss"



    gender = choose(raw_dict,"sex")

    origin = choose(raw_dict,"origins")
    originalAnimal = choose(raw_dict,"animals+human")
    fillerAnimal = choose(raw_dict,"animals")

    name = nameGen(intelligence,gender,"none")

    transmission = choose(raw_dict,"transmission")

    if lifeStage != "young":
        family = generateFamily(origin,intelligence,transmission,gender,familyname)
    else:
        family = 'none'

    if '' in family:
        family = "none"

    if origin in synth:
        robotParts,robotype = generateRobotParts()

        robotstring = ["Your synthetic parts include "]
        try:
            for i in range(len(parts)-1):
                robotstring.append("".join(\
                [robotype[i]," ",robotParts[i],", "]\
                ))
        except:
            pass
        robotstring.append("".join(\
            [robotype[-1]," ",robotParts[-1],"."]\
            ))

        if "entire body" in robotParts:
            robotstring = "You entire body is mechanised."


    body_type = choose(raw_dict,"body_type")
    body_form = choose(raw_dict,"body_form")
    childPronoun = choose(raw_dict,"family_beast")
    if intelligence == "beast" or intelligence == "hybrid":
        emotion = choose(raw_dict,"beast_emotions")
    else:
        emotion = choose(raw_dict,"emotions")
    freq = choose(raw_dict,"frequency")

    joinstring = []
    try:
        for i in range(len(parts)-1):
            joinstring.append("".join(\
            [parts[i]," of a ",animals[i],", "]\
            ))
    except:
        pass
    joinstring.append("".join(\
        [parts[-1]," of a ",animals[-1],"."]\
        ))


    joinstring = "".join(joinstring)

    print("You call yourself",name+", and are",gender+".")
    print("You have the",joinstring)

    furDensity = choose(raw_dict,"fur_density")
    furAction = choose(raw_dict,"fur_action")

    if furLocations == ["none"]:
        joinstring = "You are entirely bare of fur."
    elif furLocations == ["entire body"]:
        joinstring = ["Your whole body is covered in a ",furDensity+" of fur."]
    else:
        joinstring = ["You have a ",furDensity," of fur ",furAction," your "]
        try:
            for i in range(len(furLocations)-1):
                joinstring.append("".join(\
                [furLocations[i],", "]\
                ))
        except:
            pass
        joinstring.append("".join(\
                [furLocations[-1],"."]\
                ))

    if origin in synth:
        if random.randrange(1,2) == 1:
            furplace = ["Your body is plated in metal."]

    tfPain = False
    while tfPain == False:
        tfPain = choose(raw_dict,"transformation_pain")
    tfTime = choose(raw_dict,"time_scale")
    tfSpecific = False
    trigger = False
    mateOrigin = "finding a"
    if transmission == "biological":
        tfSpecific = choose(raw_dict,"bio_transmission")
        mateOrigin = choose(raw_dict,"mate_origins")
    elif transmission == "magical":
        tfSpecific = choose(raw_dict,"magical_transmission")
        mateOrigin = choose(raw_dict,"mate_origins")
    else:
        tfSpecific = choose(raw_dict,"bio_transmission","magical_transmission")
    if random.randrange(1,5) == 1:
        trigger = choose(raw_dict,"trigger")





    furplace = "".join(joinstring)

    ###CHILDREN

    childstring = []
    if family != "none":

        try:
            for i in range(len(family[2])-1):
                childstring.append("".join(\
                [family[2][i]+", "]\
                ))
            childstring.append("".join(\
            [family[2][-1]]\
            ))
        except:
            pass


    childstring = "".join(childstring)



    x = ""
    if origin[0] in["a","e","i","o","u"]:
        x = "n"

    y = ""
    if len(family[2]) > 1:
        y = "s"


    print("Everywhere else, you are a",fillerAnimal+". You're",age,"years old (which puts you at '"+lifeStage+"' in your lifetime), quite",body_type+", and are",body_form+".")
    print(furplace)
    if origin not in nontf:
        print("You are a{}".format(x),origin+", but originally you were a",originalAnimal+", and are about as intelligent as a",intelligence+".")
        if transmission == "none":
            pass
        else:
            if transmission == "natural":
                print("Other beings of your type exist naturally.")
            else:
                print("You can turn others into your form by",tfSpecific,"This transformation involves",tfPain,"pain, and takes",tfTime)
    else:
        print("You are a{}".format(x),origin+", and are about as intelligent as a",intelligence+".")
    if origin in synth:
        robotstring = "".join(robotstring)
        print(robotstring)
    if trigger != False:
        print("You're not always in your chimeral form, only",trigger)
    if trigger == False:
        print("During the day, you",activities[0]+",",activities[1]+" and",activities[2]+".")
    else:
        print("While in your chimeral form, you",activities[0]+",",activities[1]+" and",activities[2]+".")
    if disposition != "":
        print("You're of a",disposition,"disposition, and feel",emotion,freq+".")
    if family != "none" and transmission != "none":
        if intelligence == "beast" or intelligence == "hybrid":
            if gender == "male":
                if len(family[2]) != 0:
                    print("After",mateOrigin,"mate,",family[0]+", she bore you",len(family[2]),childPronoun+"{}".format(y)+", who you named",childstring+".")
                else:
                    print("Your have a mate named",family[0]+", who is",family[1],"in origin.")
            elif gender == "female":
                if len(family[2]) != 0:
                    print("After",mateOrigin,"mate,",family[0]+", you bore him",len(family[2]),childPronoun+"{}".format(y)+", who you named",childstring+".")
                else:
                    print("Your have a mate named",family[0]+", who is",family[1],"in origin.")
        elif intelligence == "human":
            if gender == "male":
                if len(family[2]) != 0:
                    print("After",mateOrigin,"wife,",family[0]+", she gave birth to",len(family[2]),childPronoun+"{}".format(y)+", who you named",childstring+".")
                else:
                    print("Your have a wife named",family[0]+", who is",family[1],"in origin.")
            elif gender == "female":
                if len(family[2]) != 0:
                    print("After",mateOrigin,"husband,",family[0]+", you gave birth to",len(family[2]),childPronoun+"{}".format(y)+", who you named",childstring+".")  #sorry to trigger you guys
                else:
                    print("Your have a husband named",family[0]+", who is",family[1],"in origin.")
        elif intelligence == "supernatural":
            if gender == "male":
                if len(family[2]) != 0:
                    print("After",mateOrigin,"partner,",family[0]+", she gave birth to",len(family[2]),childPronoun+"{}".format(y)+", who you named",childstring+".")
                else:
                    print("Your have a partner named",family[0]+", who is",family[1],"in origin.")
            elif gender == "female":
                if len(family[2]) != 0:
                    print("After",mateOrigin,"partner,",family[0]+", you gave birth to",len(family[2]),childPronoun+"{}".format(y)+", who you named",childstring+".")  #sorry to trigger you guys
                else:
                    print("Your have a partner named",family[0]+", who is",family[1],"in origin.")


#TODO: Height
#      Synthetic Abilities
#      Abilities in general


while True:
    if input("Press enter for a new chimera.") == "":
        print("\n")
        printOut(3)
        already_changed = []
        parts = []
        animals = []
        activities = []
        furLocations = []
        robotstring = ""
        print("\n")
