import java.util.*;

public class NodesandEdges { 

    //Generates unique IDs for every author, publisher, and printer 
    public  Map<String, String> buildIDs(ArrayList<String> allNames) {
        //Get all unique names and put them into a set

        Map<String, String> idDict = new TreeMap<String, String>();
        Set<String> uniqueNames = new HashSet<String>();

        for (int i = 0; i < allNames.size(); i++) {
            uniqueNames.add(allNames.get(i));
        }

        ArrayList<String> namesList = new ArrayList<String>(); 

        //Get according indexes so you can assign IDs
        for (String s: uniqueNames) {
            namesList.add(s);
        }

        for (int i = 0; i < namesList.size(); i++) {
            String name = namesList.get(i);
            String[] firstLast = name.split(" ");
            String tempfirst = firstLast[0];
            String templast = firstLast[1];

            if (tempfirst.length() == 1 && templast.length() == 1) {
                String first = tempfirst;
                String last = templast;
                String id = first + "." + last;
                idDict.put(namesList.get(i), id);
            }

           else if (tempfirst.length() >= 3 && templast.length() >= 3) {
                String first = tempfirst.substring(0, 3);
                String last = templast.substring(0, 3);
                String id = first + "." + last;
                idDict.put(namesList.get(i), id);
            }

            else  {
                String first = tempfirst;
                String last = templast.substring(0, 3);
                String id = first + "." + last;
                idDict.put(namesList.get(i), id); 
            }
        }
        return idDict;
    }

    public void printIDs(Map<String, String> idDict) {
        System.out.println("Label (Name), ID");
        System.out.println("------------------------");
        for (String s: idDict.keySet()) {
            System.out.println(s + "," + idDict.get(s));
        }

    }

    //Builds a dictionary that shows the relationships between different authors, publishers, and printers

    public Map<String, List<String>> buildRelationships(ArrayList<String> namePairs) {

        Map<String, List<String>> relationshipDict = new TreeMap<String, List<String>>(); 

        for (int i = 0; i < namePairs.size(); i++) {
            String[] names = namePairs.get(i).split("&"); 

            if (! relationshipDict.containsKey(names[0])) {
                relationshipDict.put(names[0], new ArrayList<String>());
            }

            relationshipDict.get(names[0]).add(names[1]);

        }

        return relationshipDict;
    }

    //Will print a column of sources, targets, and the appropriate weights given the relationships inputted 
    public void printSourceTargetWeight(Map<String, List<String>> relationshipDict, Map<String, String> idDict) {

        Set<String> sourceTargetWeightStrings = new TreeSet<String>(); 

        for(String s: relationshipDict.keySet()) {        

            for (int i = 0; i < relationshipDict.get(s).size(); i++) {
                String name1 = s;
                String name2 = relationshipDict.get(s).get(i);
                int weight = Collections.frequency(relationshipDict.get(name1), name2);

                String tempSourceTargetWeightString = idDict.get(name1) + "&" + idDict.get(name2) + "&" + weight; 
                sourceTargetWeightStrings.add(tempSourceTargetWeightString);
            }
        }
        System.out.println("Source, Target, Weight of Relationship (Frequency):");
        System.out.println("----------------------------------------------------");

        for (String s: sourceTargetWeightStrings) {
            String[] sourceTargetWeight = s.split("&");
            System.out.println(sourceTargetWeight[0] + "," + sourceTargetWeight[1] +  "," + sourceTargetWeight[2]);
        }
    }
}