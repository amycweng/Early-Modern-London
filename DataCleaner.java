import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class DataCleaner {

	public ArrayList<String> readtoList(String csvFile) {

        ArrayList<String> allNames = new ArrayList<String>();

		try {
			File file = new File(csvFile);
			FileReader fr = new FileReader(file);
			BufferedReader br = new BufferedReader(fr);

			String line = "";

			String[] tempArr;
			while ((line = br.readLine()) != null) {
				tempArr = line.split(",");
				for (String tempStr : tempArr) {
					allNames.add(tempStr);
				}
				System.out.println();
			}
			br.close();

		} catch (IOException ex) {
			ex.printStackTrace();
		}

    return allNames;
	}

    public ArrayList<String> getNamePairs(String csvFile) {
        ArrayList<String> namePairs = new ArrayList<String>(); 

        try {
			File file = new File(csvFile);
			FileReader fr = new FileReader(file);
			BufferedReader br = new BufferedReader(fr);

			String line = "";

			String[] tempArr;
			while ((line = br.readLine()) != null) {
				tempArr = line.split(",");
				String namePair = String.join("&", tempArr);
				namePairs.add(namePair);
			}
			br.close();

		} catch (IOException ex) {
			ex.printStackTrace();
		}

    return namePairs;
	}

    public static void main(String[] args) {
		// csv file to read
		String csvFile = "C:/Users/Owner/Downloads/Chapman Gephi Sheets - RAW (1).csv";
        DataCleaner trial = new DataCleaner();
		ArrayList<String> resultofAllNames = trial.readtoList(csvFile);
        NodesandEdges builderofIDs = new NodesandEdges();
        Map<String, String> idDict = builderofIDs.buildIDs(resultofAllNames);
		
		//Prints names and ID tags delimited with comma (no ugly dictionary)
		builderofIDs.printIDs(idDict);
		System.out.println();
		System.out.println("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");
		System.out.println();
		

        NodesandEdges tryRelationships = new NodesandEdges();
        DataCleaner namePairsTester = new DataCleaner();
        ArrayList<String> namePairs = namePairsTester.getNamePairs(csvFile);
        Map<String, List<String>> relationshipDict = tryRelationships.buildRelationships(namePairs);

        NodesandEdges getSourceTargetWeight = new NodesandEdges();
		//Add something to mark each list as being Source, Target, and Weight(based off of collaboration frequency)
        getSourceTargetWeight.printSourceTargetWeight(relationshipDict, idDict);
        
        
	}
}