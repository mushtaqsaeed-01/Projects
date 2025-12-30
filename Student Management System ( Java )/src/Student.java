import java.util.Scanner;
import java.util.ArrayList;
public class Student {
    String name;
    int marks;
    int id;


    Student(String n, int m, int i){
        name = n;
        marks = m;
        id = i;

    }
    static void Display(int index){
        System.out.println("Student Name: " + data.get(index).name + "\nStudent Id: " + data.get(index).id + "\nStudent Marks: " + data.get(index).marks + "\n" );
    }

    static ArrayList<Student> data = new ArrayList<>();
    static int ids = 62561;

    public static void main(String[] args){
        boolean loop = true;
        do {
            System.out.println("1. Add Student Data\n2. Search Student Data\n3. Remove Student Data\n4. Edit Student Data\n5. Exit");
            Scanner sc = new Scanner(System.in);
            int option = sc.nextInt();
            if (option > 5 || option < 1) {
                System.out.println("Please Enter the Option Between 1 to 5 !!!");
            } else {
                switch (option) {
                    case 1:
                        int checking = 0;
                        for (Student datum : data) {
                            if (datum.name == null) {
                                System.out.println("Please Enter The Student Name: ");
                                sc.nextLine();
                                datum.name = sc.nextLine();
                                System.out.println("Please Enter The Student Marks: ");
                                datum.marks = sc.nextInt();
                                System.out.println(datum.name + " Your Id Number Is " + datum.id);
                                checking = 1;
                                break;
                            }

                        }
                        if (checking != 1) {
                            System.out.println("Please Enter The Student Name: ");
                            String studentName = sc.next();
                            System.out.println("Please Enter The Student Marks: ");
                            int studentMarks = sc.nextInt();
                            data.add(new Student(studentName, studentMarks, ids));
                            System.out.println(studentName + " Your Id Number Is " + ids);
                            ids++;
                        }
                        break;

                    case 2:
                        System.out.print("Please Enter The Student Id:");
                        int checkId = sc.nextInt();
                        if (data.size() < checkId -62560 || checkId < 62561) {
                            System.out.println("This Student Data Is Not Available, Please Register The Data First");
                        } else if (data.get(checkId -62561).name == null) {
                            System.out.println("This Student Data Is Removed!! ");
                        } else {
                            Display(checkId -62561);
                        }
                        break;

                    case 3:
                        System.out.println("Please Enter The Student Id You want To Remove: ");
                        int removeId = sc.nextInt();
                        String removeStudent = data.get(removeId -62561).name;
                        data.get(removeId -62561).name = null;
                        data.get(removeId -62561).marks = 0;
                        System.out.println("The Data Of Student: \""+ removeStudent + "\" Is Removed" );
                        break;

                    case 4:
                        System.out.println("Please Enter The Id of Student You Want To Edit:");
                        int editId = sc.nextInt();
                        if (data.size() < editId-62560 || editId < 62561) {
                            System.out.println("This Student Data Is Not Available, Please Register The Data First");
                        } else {
                            Display(editId-62561);
                            System.out.println("Please Choose:\n1. Edit The Name Of Student\n2. Edit The Number Of Student");
                            int editAns = sc.nextInt();
                            if (editAns > 2 || editAns < 1){
                                System.out.println("Please Enter 1 or 2!!");
                            }
                            else {
                                switch (editAns){
                                    case 1:
                                        System.out.println("Enter The New Name:");
                                        data.get(editId-62561).name = sc.next();
                                        Display(editId-62561);
                                        break;


                                    case 2:
                                        System.out.println("Enter The New Marks:");
                                        data.get(editId-62561).marks = sc.nextInt();
                                        Display(editId-62561);
                                        break;

                                }
                            }
                        }
                        break;


                    case 5:
                        loop = false;
                        break;

                }

            }
        }while (loop);

    }
}