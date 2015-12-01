import java.util.*;
import java.io.*;

public class ScheduleParser {

	public String parse() {
	
		File file = new File("schedule.txt");
		String token = "";

		try {
			Scanner sc = new Scanner(file);
			while (sc.hasNextLine()) {
				String temp = sc.nextLine();
				if (temp.equals("LEC") || temp.equals("TUT")) {
					temp = sc.nextLine();
					temp = temp.replaceAll("\\s", "");
					temp = temp.replace(":", "");
					token += temp + " ";
				}
			}
			sc.close();
			return token;
		}	
	
		catch (FileNotFoundException e) {
			System.out.println("file error");
			return token;
		}
	}
}
