# -*- coding: utf-8 -*-
import json

class LoadIl2cppDumperScript:
    def __init__(self):
        self.document = Document.getCurrentDocument()
        segments = self.document.getSegmentsList()
        self.starting_address = segments[0].getStartingAddress()
        
    def get_address(self, addr):
        return self.starting_address + addr
        
    def process_script(self, script_path):
        with open(script_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if "ScriptMethod" in data:
            self.process_script_methods(data["ScriptMethod"])

        if "ScriptString" in data:
            self.process_script_strings(data["ScriptString"])

        if "ScriptMetadata" in data:
            self.process_script_metadata(data["ScriptMetadata"])

        if "ScriptMetadataMethod" in data:
            self.process_script_metadata_methods(data["ScriptMetadataMethod"])

        print("Script finished!")

    def replace_null_characters(self, string):
        return string.replace("\x00", "")

    def process_script_methods(self, script_methods):
        for script_method in script_methods:
            address = self.get_address(script_method["Address"])
            current_method_name = self.document.getNameAtAddress(address)
            self.document.setNameAtAddress(address, script_method["Name"])
            print(f"Renamed {current_method_name} at {address} to {script_method['Name']}")

    def process_script_strings(self, script_strings):
        for index, script_string in enumerate(script_strings, start=1):
            address = self.get_address(script_string["Address"])

            current_string_name = self.document.getNameAtAddress(address)
            new_string_name = f"StringLiteral_{index}"
            
            self.document.setNameAtAddress(address, new_string_name)
            print(f"Renamed {current_string_name} at {address} to {new_string_name}")

            segment = self.document.getSegmentAtAddress(address)
            if segment:
                inline_comment = self.replace_null_characters(script_string["Value"])
                segment.setInlineCommentAtAddress(address, inline_comment)
                print(f"Set inline comment at address {address} to {inline_comment}")

    def process_script_metadata(self, script_metadata):
        for meta in script_metadata:
            address = self.get_address(meta["Address"])
            self.document.setNameAtAddress(address, meta["Name"])
            print(f"Set name at address {address} to {meta['Name']}")

            segment = self.document.getSegmentAtAddress(address)
            if segment:
                inline_comment = self.replace_null_characters(meta["Name"])
                segment.setInlineCommentAtAddress(address, inline_comment)
                print(f"Set inline comment at address {address} to {inline_comment}")

    def process_script_metadata_methods(self, script_metadata_methods):
        for meta_method in script_metadata_methods:
            address = self.get_address(meta_method["Address"])
            self.document.setNameAtAddress(address, meta_method["Name"])
            print(f"Set name at address {address} to {meta_method['Name']}")

            # Set inline comments
            segment = self.document.getSegmentAtAddress(address)
            if segment:
                inline_comment = self.replace_null_characters(meta_method["Name"])
                segment.setInlineCommentAtAddress(address, inline_comment)
                print(f"Set inline comment at address {address} to {inline_comment}")

                inline_comment_method_address = '{0:X}'.format(self.get_address(meta_method["MethodAddress"]))
                segment.setInlineCommentAtAddress(address, inline_comment_method_address)
                print(f"Set inline comment at address {address} to {inline_comment_method_address}")

    def run(self):
        script_path = self.document.askFile("Choose the script.json from Il2cppdumper", "false", None)

        if not script_path:
            raise Exception("No file selected")
        
        self.process_script(script_path)


LoadIl2cppDumperScript().run()
