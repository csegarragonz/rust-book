fn main() {
    let s = String::from("Hello world!");

    let slice = first_word(&s);

    println!("Slice from {s} is: {slice}");
}

fn first_word(s: &String) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}
